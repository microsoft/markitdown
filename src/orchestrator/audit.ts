import { lstat, open, realpath, writeFile } from "node:fs/promises";
import { basename, dirname, extname, isAbsolute, join, resolve, sep } from "node:path";
import { z } from "zod";
import type {
  AnalysisUnit,
  AuditRun,
  BackendName,
  BugFinding,
  PatchAttempt,
  TargetInfo,
  ValidationCommandSpec,
  ValidationResult
} from "../domain/types.js";
import { GhClient } from "../github/gh.js";
import { GitClient } from "../git/git.js";
import { OutputStore, type WithheldCandidateRecord } from "../output/store.js";
import { shortHash, stableArtifactPathSegment } from "../output/safePath.js";
import { applyFileEdits, type FileEdit } from "../patch/applyPatch.js";
import {
  createAgentProvider,
  requireProviderAvailable,
  type JsonAgentProvider
} from "../providers/provider.js";
import {
  evaluatePrQuality,
  selectFinalPrCandidate,
  type PrCandidate
} from "../quality/prQuality.js";
import { renderAuditReport, type AuditReportInput } from "../report/report.js";
import { scanRepository } from "../scanner/scanner.js";
import { runCommand, truncateUtf8, type CommandRunner } from "../shared/command.js";
import { createLogger, type Logger } from "../shared/logger.js";
import { resolveTarget } from "../target/target.js";
import { runValidation } from "../validation/validation.js";

export interface RunAuditOptions {
  backend: BackendName;
  target: string;
  outputDir: string;
  rootDir?: string;
  now?: Date;
  runner?: CommandRunner;
  providerFactory?: (backend: BackendName, model?: string) => JsonAgentProvider;
  gitClient?: Pick<GitClient, "commitAll" | "setRemote" | "pushBranch">;
  pullRequestClient?: Pick<GhClient, "currentUsername" | "ensureFork" | "createPullRequest">;
  skipProviderAvailability?: boolean;
  logger?: Logger;
  model?: string;
  maxUnits?: number;
}

export interface RunAuditResult {
  outputDir: string;
  targetRepo: string;
  openedPullRequests: string[];
  reportPath: string;
}

interface PatchCandidate extends PrCandidate {
  edits: FileEdit[];
  validationCommands: ValidationCommandSpec[];
}

interface TextSnippet {
  path: string;
  text: string;
  truncated: boolean;
  sizeBytes: number;
}

interface UnitSourceContext {
  source?: TextSnippet;
  relatedTests: TextSnippet[];
}

interface DiffContext {
  command: string;
  text: string;
  truncated: boolean;
  available: boolean;
}

interface PinnedBase {
  commit: string;
}

const maxContextBytes = 64 * 1024;
const maxDiffBytes = 128 * 1024;
const maxRelatedTests = 3;
const diffTimeoutMs = 30 * 1000;
const maxFindingsPerUnit = 10;
const PrQualityRubric = {
  bugValue: "0-30: impact, exploitability/user harm, and bug importance.",
  evidenceStrength: "0-25: concrete reproduction, source evidence, and confidence.",
  patchQuality: "0-20: minimality, correctness, maintainability, and low blast radius.",
  validation: "0-15: relevant automated/manual validation and clean diff checks.",
  maintainerFit: "0-10: aligns with repository style, scope, and likely maintainer acceptance.",
  total: "0-100: sum of the five component scores."
} as const;
const PrQualityPrompt = [
  "Score this PR candidate. Return structured scores and hard rejection flags.",
  "Use this exact 100-point rubric:",
  "bugValue: 0-30",
  "evidenceStrength: 0-25",
  "patchQuality: 0-20",
  "validation: 0-15",
  "maintainerFit: 0-10",
  "total: 0-100, equal to the sum of all component scores.",
  "Reject with hardRejections when the bug is not concrete, the patch is broad/risky, validation is missing, or the change is unlikely to be accepted."
].join("\n");

export async function runAudit(options: RunAuditOptions): Promise<RunAuditResult> {
  const now = options.now ?? new Date();
  const runner = options.runner ?? runCommand;
  const logger = options.logger ?? createLogger("info");

  logger.info(`starting audit: backend=${options.backend} target=${options.target}`);

  if (!options.skipProviderAvailability) {
    await requireProviderAvailable(options.backend);
  }

  const provider = options.providerFactory?.(options.backend, options.model) ?? createAgentProvider(options.backend, { model: options.model });
  void provider;

  const target = await resolveTarget({
    target: options.target,
    outputDir: options.outputDir,
    runner
  });
  logger.info(`target resolved: ${target.repo} at ${target.localPath}`);

  const store = await OutputStore.create(options.outputDir, now);
  const run: AuditRun = {
    id: formatRunId(now),
    backend: options.backend,
    startedAt: now.toISOString()
  };

  await store.writeRun(run);

  await store.writeTarget(target);

  const pinnedBase = await resetTargetWorkspace(runner, target);
  const units = await scanRepository({ rootDir: target.localPath, maxFiles: options.maxUnits });
  logger.info(`scanned ${units.length} unit(s)`);
  await store.writeUnits(units);
  const candidates: PatchCandidate[] = [];
  const withheldCandidates: WithheldCandidateRecord[] = [];
  const seenFindingIds = new Set<string>();
  let findingsCount = 0;
  let rejectedFindings = 0;
  const prReviews: AuditReportInput["prReviews"] = [];

  for (const unit of units) {
    logger.debug(`auditing unit: ${unit.id}`);
    const unitContext = await buildUnitSourceContext(target.localPath, unit);
    const audit = await provider.runJson({
      stage: "unit-audit",
      prompt: "Audit this analysis unit for concrete high-value bugs. Return findings only.",
      context: { target, unit, ...unitContext },
      schema: AuditSchema,
      jsonSchema: AuditJsonSchema,
      onEvent: store.appendAgentEvent
    });
    logger.info(`unit ${unit.id}: ${audit.data.findings.length} finding(s)`);

    for (const rawFinding of audit.data.findings.slice(0, maxFindingsPerUnit)) {
      const finding = namespaceFinding(rawFinding, unit, seenFindingIds);
      findingsCount += 1;
      logger.info(`processing finding ${finding.id}: ${finding.title}`);
      await store.appendFinding(finding);

      try {
        const bugReview = await provider.runJson({
          stage: "bug-review",
          prompt: "Review this bug candidate. Approve only concrete, valuable bugs worth patching.",
          context: { target, unit, ...unitContext, finding },
          schema: BugReviewSchema,
          jsonSchema: BugReviewJsonSchema,
          onEvent: store.appendAgentEvent
        });

        const bugReviewData = { ...bugReview.data, findingId: finding.id };
        await store.appendBugReview(bugReviewData);

        if (bugReviewData.decision === "reject") {
          rejectedFindings += 1;
          logger.info(`finding ${finding.id}: rejected by bug-review`);
          continue;
        }

        const patch = await provider.runJson({
          stage: "patch",
          prompt: "Create a minimal bug-fix patch. Return whole-file edits only.",
          context: { target, unit, ...unitContext, finding, bugReview: bugReviewData },
          schema: PatchSchema,
          jsonSchema: PatchJsonSchema,
          onEvent: store.appendAgentEvent
        });

        const branch = `aoc/${run.id}/${branchSlug(finding.id)}`;
        const validationCommands = normalizeValidationCommands(patch.data.validationCommands);
        await resetTargetWorkspace(runner, target, pinnedBase);
        const checkout = await runner("git", ["checkout", "-B", branch], { cwd: target.localPath });
        if (checkout.exitCode !== 0) {
          throw new Error(`Failed to create patch branch ${branch}: ${checkout.stderr || checkout.stdout}`);
        }

        logger.debug(`finding ${finding.id}: applied patch on ${branch}`);
        const changedFiles = await applyFileEdits(target.localPath, patch.data.edits);
        const validation = await runValidation({
          findingId: finding.id,
          repoPath: target.localPath,
          outputDir: options.outputDir,
          commands: [
            { command: "git", args: ["diff", "--check"] },
            ...validationCommands
          ],
          runner
        });
        const diff = await captureGitDiff(runner, target.localPath);
        const attempt: PatchAttempt = {
          findingId: finding.id,
          branch,
          title: patch.data.title,
          body: patch.data.body,
          changedFiles,
          diffSummary: renderPatchAttemptDiff(validation, diff)
        };

        await store.writePatchAttempt(attempt);
        await store.appendValidation(validation);
        logger.debug(`finding ${finding.id}: validation status=${validation.status}`);

        const quality = await provider.runJson({
          stage: "pr-quality-review",
          prompt: PrQualityPrompt,
          context: { target, finding, bugReview: bugReviewData, patchAttempt: attempt, validation, diff, qualityRubric: PrQualityRubric },
          schema: PrQualityReviewSchema,
          jsonSchema: PrQualityReviewJsonSchema,
          onEvent: store.appendAgentEvent
        });

        const qualityData = { ...quality.data, findingId: finding.id };
        await store.appendPrQualityReview(qualityData);
        prReviews.push({
          findingId: qualityData.findingId,
          total: qualityData.scores.total,
          decision: qualityData.decision,
          hardRejections: qualityData.hardRejections,
          summary: qualityData.summary
        });

        const qualityDecision = evaluatePrQuality(qualityData);
        logger.info(
          `finding ${finding.id}: quality score=${qualityData.scores.total} decision=${qualityData.decision} allowed=${qualityDecision.allowed}`
        );
        if (qualityData.decision === "submit_candidate" && qualityDecision.allowed) {
          if (validationPassed(validation)) {
            candidates.push({ review: qualityData, patch: attempt, edits: patch.data.edits, validationCommands });
          } else {
            withheldCandidates.push({
              findingId: attempt.findingId,
              branch: attempt.branch,
              title: attempt.title,
              qualityScore: qualityData.scores.total,
              reason: validationFailureReason(validation)
            });
          }
        } else {
          withheldCandidates.push({
            findingId: attempt.findingId,
            branch: attempt.branch,
            title: attempt.title,
            qualityScore: qualityData.scores.total,
            reason:
              qualityData.decision === "reject"
                ? `quality rejected: ${qualityData.hardRejections[0] ?? qualityData.summary ?? qualityDecision.reason}`
                : qualityDecision.reason
          });
        }
      } catch (error) {
        const message = error instanceof Error ? error.message : String(error);
        logger.warn(`finding ${finding.id}: error during processing: ${message}`);
        withheldCandidates.push({
          findingId: finding.id,
          branch: `aoc/${run.id}/${branchSlug(finding.id)}`,
          title: finding.title,
          qualityScore: 0,
          reason: `audit error: ${message}`
        });
        try {
          await resetTargetWorkspace(runner, target, pinnedBase);
        } catch {
          // ignore reset failure and continue to next finding
        }
      }
    }
  }

  logger.info(`audit loop complete: ${candidates.length} candidate(s), ${withheldCandidates.length} withheld`);

  const openedPullRequests: string[] = [];
  const selection = selectFinalPrCandidate(candidates);
  const gitClient = options.gitClient ?? new GitClient(runner);
  const pullRequestClient = options.pullRequestClient ?? new GhClient(runner);

  if (selection.selected !== undefined) {
    logger.info(`opening PR for finding ${selection.selected.patch.findingId}`);
    const opened = await openSelectedPullRequest({
      selected: selection.selected as PatchCandidate,
      target,
      outputDir: options.outputDir,
      runner,
      gitClient,
      pullRequestClient,
      store,
      pinnedBase
    });
    if ("url" in opened) {
      openedPullRequests.push(opened.url);
      logger.info(`PR opened: ${opened.url}`);
    } else {
      withheldCandidates.push(opened.withheld);
      logger.warn(`PR withheld: ${opened.withheld.reason}`);
    }
  }

  for (const candidate of selection.withheld) {
    withheldCandidates.push({
      findingId: candidate.patch.findingId,
      branch: candidate.patch.branch,
      title: candidate.patch.title,
      qualityScore: candidate.review.scores.total,
      reason: "not selected within one-PR run budget"
    });
  }

  for (const candidate of withheldCandidates) {
    await store.appendWithheldCandidate(candidate);
  }

  run.completedAt = new Date().toISOString();
  await store.writeRun(run);

  const reportPath = join(options.outputDir, "reports", "summary.md");
  await writeFile(
    reportPath,
    renderAuditReport({
      targetRepo: target.repo,
      backend: options.backend,
      unitsAnalyzed: units.length,
      findingsCount,
      rejectedFindings,
      prReviews,
      openedPullRequests,
      withheldCount: withheldCandidates.length
    })
  );

  logger.info(
    `audit complete: units=${units.length} findings=${findingsCount} rejected=${rejectedFindings} PRs=${openedPullRequests.length} withheld=${withheldCandidates.length}`
  );

  return {
    outputDir: options.outputDir,
    targetRepo: target.repo,
    openedPullRequests,
    reportPath
  };
}

export function formatRunId(date: Date): string {
  return date.toISOString().slice(0, 23).replace(/[-:T.]/g, "");
}

const FindingSchema = z.object({
  id: z.string(),
  unitId: z.string(),
  title: z.string(),
  severity: z.enum(["low", "medium", "high", "critical"]),
  affectedBehavior: z.string().optional(),
  rootCause: z.string().optional(),
  reproduction: z.string().optional(),
  suggestedValidation: z.string().optional()
});

const AuditSchema = z.object({
  findings: z.array(FindingSchema)
});

const BugReviewSchema = z.object({
  findingId: z.string(),
  decision: z.enum(["approve_for_patch", "reject"]),
  bugValue: z.number(),
  evidenceStrength: z.number(),
  reason: z.string(),
  patchStrategy: z.string().optional()
});

const PatchSchema = z.object({
  title: z.string(),
  body: z.string(),
  edits: z.array(
    z.object({
      path: z.string(),
      content: z.string()
    })
  ),
  validationCommands: z.array(
    z.object({
      command: z.string(),
      args: z.array(z.string()).default([])
    })
  )
});

const PrQualityReviewSchema = z.object({
  findingId: z.string(),
  decision: z.enum(["submit_candidate", "reject"]),
  scores: z.object({
    bugValue: z.number().min(0).max(30),
    evidenceStrength: z.number().min(0).max(25),
    patchQuality: z.number().min(0).max(20),
    validation: z.number().min(0).max(15),
    maintainerFit: z.number().min(0).max(10),
    total: z.number().min(0).max(100)
  }).superRefine((scores, context) => {
    const expectedTotal =
      scores.bugValue +
      scores.evidenceStrength +
      scores.patchQuality +
      scores.validation +
      scores.maintainerFit;
    if (Math.abs(scores.total - expectedTotal) > 0.001) {
      context.addIssue({
        code: z.ZodIssueCode.custom,
        path: ["total"],
        message: "total must equal the sum of all component scores"
      });
    }
  }),
  hardRejections: z.array(z.string()),
  summary: z.string(),
  maintainerExplanation: z.string()
});

const FindingJsonSchema = {
  type: "object",
  required: ["id", "unitId", "title", "severity"],
  additionalProperties: false,
  properties: {
    id: { type: "string" },
    unitId: { type: "string" },
    title: { type: "string" },
    severity: { enum: ["low", "medium", "high", "critical"] },
    affectedBehavior: { type: "string" },
    rootCause: { type: "string" },
    reproduction: { type: "string" },
    suggestedValidation: { type: "string" }
  }
} as const;

const AuditJsonSchema = {
  type: "object",
  required: ["findings"],
  additionalProperties: false,
  properties: {
    findings: {
      type: "array",
      items: FindingJsonSchema
    }
  }
} as const;

const BugReviewJsonSchema = {
  type: "object",
  required: ["findingId", "decision", "bugValue", "evidenceStrength", "reason"],
  additionalProperties: false,
  properties: {
    findingId: { type: "string" },
    decision: { enum: ["approve_for_patch", "reject"] },
    bugValue: { type: "number" },
    evidenceStrength: { type: "number" },
    reason: { type: "string" },
    patchStrategy: { type: "string" }
  }
} as const;

const FileEditJsonSchema = {
  type: "object",
  required: ["path", "content"],
  additionalProperties: false,
  properties: {
    path: { type: "string" },
    content: { type: "string" }
  }
} as const;

const ValidationCommandJsonSchema = {
  type: "object",
  required: ["command", "args"],
  additionalProperties: false,
  properties: {
    command: {
      enum: ["git", "npm", "pnpm", "yarn", "bun", "node", "npx", "python", "python3", "pytest", "go", "cargo"]
    },
    args: {
      type: "array",
      items: { type: "string" }
    }
  }
} as const;

const PatchJsonSchema = {
  type: "object",
  required: ["title", "body", "edits", "validationCommands"],
  additionalProperties: false,
  properties: {
    title: { type: "string" },
    body: { type: "string" },
    edits: {
      type: "array",
      items: FileEditJsonSchema
    },
    validationCommands: {
      type: "array",
      items: ValidationCommandJsonSchema
    }
  }
} as const;

const PrQualityScoresJsonSchema = {
  type: "object",
  required: ["bugValue", "evidenceStrength", "patchQuality", "validation", "maintainerFit", "total"],
  additionalProperties: false,
  properties: {
    bugValue: { type: "number", minimum: 0, maximum: 30 },
    evidenceStrength: { type: "number", minimum: 0, maximum: 25 },
    patchQuality: { type: "number", minimum: 0, maximum: 20 },
    validation: { type: "number", minimum: 0, maximum: 15 },
    maintainerFit: { type: "number", minimum: 0, maximum: 10 },
    total: { type: "number", minimum: 0, maximum: 100 }
  }
} as const;

const PrQualityReviewJsonSchema = {
  type: "object",
  required: ["findingId", "decision", "scores", "hardRejections", "summary", "maintainerExplanation"],
  additionalProperties: false,
  properties: {
    findingId: { type: "string" },
    decision: { enum: ["submit_candidate", "reject"] },
    scores: PrQualityScoresJsonSchema,
    hardRejections: {
      type: "array",
      items: { type: "string" }
    },
    summary: { type: "string" },
    maintainerExplanation: { type: "string" }
  }
} as const;

function branchSlug(value: string): string {
  const slugged = value
    .toLowerCase()
    .replace(/[^a-z0-9]+/g, "-")
    .replace(/^-+|-+$/g, "");
  const safeSlug = slugged || "finding";
  if (safeSlug === value) {
    return safeSlug;
  }

  return `${safeSlug}_${shortHash(value)}`;
}

function namespaceFinding(finding: BugFinding, unit: AnalysisUnit, seenFindingIds: Set<string>): BugFinding {
  const uniqueId = uniqueFindingId(finding.id, unit, seenFindingIds);
  return uniqueId === finding.id ? finding : { ...finding, id: uniqueId };
}

function uniqueFindingId(id: string, unit: AnalysisUnit, seenFindingIds: Set<string>): string {
  if (!seenFindingIds.has(id)) {
    seenFindingIds.add(id);
    return id;
  }

  const namespace = unit.path || unit.id;
  let candidate = `${id}@${namespace}`;
  let counter = 2;
  while (seenFindingIds.has(candidate)) {
    candidate = `${id}@${namespace}#${counter}`;
    counter += 1;
  }

  seenFindingIds.add(candidate);
  return candidate;
}

function normalizeValidationCommands(commands: Array<{ command: string; args?: string[] }>): ValidationCommandSpec[] {
  return commands.map((command) => ({
    command: command.command,
    args: command.args ?? []
  }));
}

function validationPassed(validation: { status: string; commands: Array<{ exitCode: number }> }): boolean {
  return validation.status === "passed" && validation.commands.every((command) => command.exitCode === 0);
}

function validationFailureReason(validation: { status: string; commands: Array<{ command: string; exitCode: number }> }): string {
  const failedCommands = validation.commands
    .filter((command) => command.exitCode !== 0)
    .map((command) => `${command.command} exited ${command.exitCode}`);

  if (failedCommands.length > 0) {
    return `validation failed: ${failedCommands.join("; ")}`;
  }

  return `validation failed with status ${validation.status}`;
}

async function buildUnitSourceContext(rootDir: string, unit: AnalysisUnit): Promise<UnitSourceContext> {
  const source = await readSnippet(rootDir, unit.path, maxContextBytes);
  const relatedTests = await readRelatedTestSnippets(rootDir, unit, maxRelatedTests);

  return { source, relatedTests };
}

async function readRelatedTestSnippets(
  rootDir: string,
  unit: AnalysisUnit,
  limit: number
): Promise<TextSnippet[]> {
  const snippets: TextSnippet[] = [];
  const seen = new Set<string>();

  for (const candidate of relatedTestCandidates(unit.path)) {
    if (seen.has(candidate)) {
      continue;
    }
    seen.add(candidate);

    const snippet = await readSnippet(rootDir, candidate, maxContextBytes);
    if (snippet !== undefined) {
      snippets.push(snippet);
    }
    if (snippets.length >= limit) {
      break;
    }
  }

  return snippets;
}

function relatedTestCandidates(unitPath: string): string[] {
  const extension = extname(unitPath);
  const fileName = basename(unitPath, extension);
  const unitDir = dirname(unitPath);
  const withoutSourcePrefix = unitPath.replace(/^(src|lib|app)\//, "");
  const withoutExtension = extension.length > 0 ? withoutSourcePrefix.slice(0, -extension.length) : withoutSourcePrefix;
  const testExtensions = [".test", ".spec"];
  const candidates: string[] = [];

  for (const suffix of testExtensions) {
    candidates.push(`tests/${withoutExtension}${suffix}${extension}`);
    candidates.push(`test/${withoutExtension}${suffix}${extension}`);
    candidates.push(`__tests__/${withoutExtension}${suffix}${extension}`);
    candidates.push(`tests/${fileName}${suffix}${extension}`);
    candidates.push(`${unitDir}/${fileName}${suffix}${extension}`);
  }

  return candidates;
}

async function readSnippet(rootDir: string, relativePath: string, maxBytes: number): Promise<TextSnippet | undefined> {
  const absolutePath = safeResolveUnderRoot(rootDir, relativePath);
  if (absolutePath === undefined) {
    return undefined;
  }

  try {
    const stats = await lstat(absolutePath);
    if (!stats.isFile()) {
      return undefined;
    }

    const [realRoot, realFile] = await Promise.all([realpath(rootDir), realpath(absolutePath)]);
    if (!isPathInsideRoot(realRoot, realFile)) {
      return undefined;
    }

    const { text, truncated } = await readBoundedText(realFile, maxBytes);
    return {
      path: relativePath,
      text,
      truncated,
      sizeBytes: stats.size
    };
  } catch {
    return undefined;
  }
}

async function readBoundedText(filePath: string, maxBytes: number): Promise<{ text: string; truncated: boolean }> {
  const file = await open(filePath, "r");
  try {
    const buffer = Buffer.alloc(maxBytes + 1);
    const { bytesRead } = await file.read(buffer, 0, buffer.length, 0);
    const truncated = bytesRead > maxBytes;
    let end = truncated ? maxBytes : bytesRead;
    if (truncated) {
      while (end > 0 && (buffer[end] & 0xc0) === 0x80) {
        end -= 1;
      }
    }
    const text = buffer.subarray(0, end).toString("utf8");
    return { text, truncated };
  } finally {
    await file.close();
  }
}

function isPathInsideRoot(rootDir: string, filePath: string): boolean {
  const root = resolve(rootDir);
  const absolutePath = resolve(filePath);
  const prefix = root.endsWith(sep) ? root : `${root}${sep}`;
  return absolutePath !== root && absolutePath.startsWith(prefix);
}

function safeResolveUnderRoot(rootDir: string, relativePath: string): string | undefined {
  if (isAbsolute(relativePath)) {
    return undefined;
  }

  const root = resolve(rootDir);
  const absolutePath = resolve(root, relativePath);
  const prefix = root.endsWith(sep) ? root : `${root}${sep}`;
  if (absolutePath !== root && absolutePath.startsWith(prefix)) {
    return absolutePath;
  }

  return undefined;
}

async function captureGitDiff(runner: CommandRunner, repoPath: string): Promise<DiffContext> {
  const command = "git diff --no-ext-diff";
  const result = await runner("git", ["diff", "--no-ext-diff"], {
    cwd: repoPath,
    timeoutMs: diffTimeoutMs,
    maxOutputBytes: maxDiffBytes
  });

  if (result.exitCode !== 0) {
    const text = result.stderr || result.stdout;
    return {
      command,
      text: truncateText(text, maxDiffBytes),
      truncated: Buffer.byteLength(text, "utf8") > maxDiffBytes,
      available: false
    };
  }

  return {
    command,
    text: truncateText(result.stdout, maxDiffBytes),
    truncated: Buffer.byteLength(result.stdout, "utf8") > maxDiffBytes,
    available: true
  };
}

function renderPatchAttemptDiff(validation: ValidationResult, diff: DiffContext): string {
  const sections = [`Validation:\n${validation.diffSummary}`];

  if (diff.available && diff.text.trim() !== "") {
    sections.push(`Diff (${diff.command}${diff.truncated ? ", truncated" : ""}):\n${diff.text}`);
  } else if (diff.available) {
    sections.push(`Diff (${diff.command}): no changes captured.`);
  } else {
    sections.push(`Diff unavailable (${diff.command}${diff.truncated ? ", truncated" : ""}):\n${diff.text}`);
  }

  return sections.join("\n\n");
}

function truncateText(text: string, maxBytes: number): string {
  return truncateUtf8(text, maxBytes);
}

async function resetTargetWorkspace(
  runner: CommandRunner,
  target: TargetInfo,
  pinnedBase?: PinnedBase
): Promise<PinnedBase> {
  const baseRef = pinnedBase?.commit ?? `${target.baseRemote}/${target.baseBranch}`;
  if (pinnedBase === undefined) {
    await runRequiredGitStep(runner, target, ["fetch", target.baseRemote]);
  }
  await runRequiredGitStep(runner, target, ["checkout", "-B", target.baseBranch, baseRef]);
  await runRequiredGitStep(runner, target, ["reset", "--hard", baseRef]);
  await runRequiredGitStep(runner, target, ["clean", "-fd"]);
  return pinnedBase ?? { commit: await readHeadCommit(runner, target) };
}

async function runRequiredGitStep(runner: CommandRunner, target: TargetInfo, args: string[]): Promise<void> {
  const result = await runner("git", args, { cwd: target.localPath });

  if (result.exitCode !== 0) {
    throw new Error(`Failed to reset target workspace with git ${args.join(" ")}: ${result.stderr || result.stdout}`);
  }
}

async function readHeadCommit(runner: CommandRunner, target: TargetInfo): Promise<string> {
  const result = await runner("git", ["rev-parse", "HEAD"], { cwd: target.localPath });
  if (result.exitCode !== 0) {
    throw new Error(`Failed to resolve target base commit: ${result.stderr || result.stdout}`);
  }

  const commit = result.stdout.trim();
  if (commit.length === 0) {
    throw new Error("Failed to resolve target base commit: empty git rev-parse output");
  }

  return commit;
}

async function checkRemoteBaseStillPinned(
  runner: CommandRunner,
  target: TargetInfo,
  pinnedBase: PinnedBase
): Promise<{ ok: true } | { ok: false; reason: string }> {
  const branchRef = `refs/heads/${target.baseBranch}`;
  const result = await runner("git", ["ls-remote", target.baseRemote, branchRef], { cwd: target.localPath });
  if (result.exitCode !== 0) {
    return {
      ok: false,
      reason: `base branch check failed: ${result.stderr || result.stdout}`
    };
  }

  const remoteCommit = parseLsRemoteCommit(result.stdout);
  if (remoteCommit === undefined) {
    return {
      ok: false,
      reason: `base branch check failed: ${target.baseRemote}/${target.baseBranch} was not found`
    };
  }

  if (remoteCommit !== pinnedBase.commit) {
    return {
      ok: false,
      reason: `base branch moved from ${pinnedBase.commit} to ${remoteCommit}`
    };
  }

  return { ok: true };
}

function parseLsRemoteCommit(output: string): string | undefined {
  const [commit] = output.trim().split(/\s+/, 1);
  return commit === "" ? undefined : commit;
}

async function openSelectedPullRequest(options: {
  selected: PatchCandidate;
  target: TargetInfo;
  outputDir: string;
  runner: CommandRunner;
  gitClient: Pick<GitClient, "commitAll" | "setRemote" | "pushBranch">;
  pullRequestClient: Pick<GhClient, "currentUsername" | "ensureFork" | "createPullRequest">;
  store: OutputStore;
  pinnedBase: PinnedBase;
}): Promise<{ url: string } | { withheld: WithheldCandidateRecord }> {
  await resetTargetWorkspace(options.runner, options.target, options.pinnedBase);
  const checkout = await options.runner("git", ["checkout", "-B", options.selected.patch.branch], {
    cwd: options.target.localPath
  });
  if (checkout.exitCode !== 0) {
    throw new Error(
      `Failed to create selected PR branch ${options.selected.patch.branch}: ${checkout.stderr || checkout.stdout}`
    );
  }
  const changedFiles = await applyFileEdits(options.target.localPath, options.selected.edits);
  const validation = await runValidation({
    findingId: options.selected.patch.findingId,
    repoPath: options.target.localPath,
    outputDir: options.outputDir,
    commands: [{ command: "git", args: ["diff", "--check"] }, ...options.selected.validationCommands],
    runner: options.runner
  });
  const diff = await captureGitDiff(options.runner, options.target.localPath);
  const finalAttempt: PatchAttempt = {
    ...options.selected.patch,
    changedFiles,
    diffSummary: renderPatchAttemptDiff(validation, diff)
  };

  await options.store.writePatchAttempt(finalAttempt);
  await options.store.appendValidation(validation);

  if (!validationPassed(validation)) {
    const withheld = {
      withheld: {
        findingId: finalAttempt.findingId,
        branch: finalAttempt.branch,
        title: finalAttempt.title,
        qualityScore: options.selected.review.scores.total,
        reason: `final validation failed: ${validationFailureReason(validation)}`
      }
    };
    await cleanupPrBranch(options.runner, options.target, options.selected.patch.branch);
    return withheld;
  }

  const baseCheck = await checkRemoteBaseStillPinned(options.runner, options.target, options.pinnedBase);
  if (!baseCheck.ok) {
    const withheld = {
      withheld: {
        findingId: finalAttempt.findingId,
        branch: finalAttempt.branch,
        title: finalAttempt.title,
        qualityScore: options.selected.review.scores.total,
        reason: baseCheck.reason
      }
    };
    await cleanupPrBranch(options.runner, options.target, options.selected.patch.branch);
    return withheld;
  }

  const username = await options.pullRequestClient.currentUsername();
  await options.pullRequestClient.ensureFork(options.target.owner, options.target.name);
  await options.gitClient.setRemote(
    options.target.localPath,
    "aoc-fork",
    `https://github.com/${username}/${options.target.name}.git`
  );

  const artifactFindingId = stableArtifactPathSegment(options.selected.patch.findingId, "finding");
  const bodyFile = join(options.outputDir, "patch-attempts", `${artifactFindingId}-pr-body.md`);
  await writeFile(bodyFile, finalAttempt.body);

  await options.gitClient.commitAll(options.target.localPath, finalAttempt.title);
  await options.gitClient.pushBranch(options.target.localPath, "aoc-fork", finalAttempt.branch);
  const url = await options.pullRequestClient.createPullRequest({
    owner: options.target.owner,
    name: options.target.name,
    head: `${username}:${finalAttempt.branch}`,
    base: options.target.defaultBranch,
    title: finalAttempt.title,
    bodyFile
  });

  await options.store.appendPullRequest({
    findingId: finalAttempt.findingId,
    branch: finalAttempt.branch,
    title: finalAttempt.title,
    url,
    qualityScore: options.selected.review.scores.total
  });

  await cleanupPrBranch(options.runner, options.target, options.selected.patch.branch);
  return { url };
}

async function cleanupPrBranch(
  runner: CommandRunner,
  target: TargetInfo,
  branch: string
): Promise<void> {
  await runner("git", ["checkout", "-B", target.baseBranch], { cwd: target.localPath });
  await runner("git", ["branch", "-D", branch], { cwd: target.localPath });
}
