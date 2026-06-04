import { mkdir, writeFile } from "node:fs/promises";
import { join } from "node:path";
import type { ValidationCommand, ValidationCommandSpec, ValidationResult } from "../domain/types.js";
import { stableArtifactPathSegment } from "../output/safePath.js";
import { runCommand, truncateUtf8, type CommandRunner } from "../shared/command.js";

export interface RunValidationOptions {
  findingId: string;
  repoPath: string;
  outputDir: string;
  commands: ValidationCommandSpec[];
  runner?: CommandRunner;
}

interface RecordedCommand extends ValidationCommand {
  command: string;
  error?: string;
}

const allowedValidationCommands = new Set([
  "git",
  "npm",
  "pnpm",
  "yarn",
  "bun",
  "node",
  "npx",
  "python",
  "python3",
  "pytest",
  "go",
  "cargo"
]);
const validationTimeoutMs = 5 * 60 * 1000;
const validationOutputLimitBytes = 256 * 1024;
const shellMetacharacterPattern = /[;&|<>'"\n\r\0$`(){}[\]*?]/;

export async function runValidation(options: RunValidationOptions): Promise<ValidationResult> {
  const runner = options.runner ?? runCommand;
  const artifactFindingId = stableArtifactPathSegment(options.findingId, "finding");
  const validationDir = join(options.outputDir, "validation", artifactFindingId);
  await mkdir(validationDir, { recursive: true });

  const commands: RecordedCommand[] = [];
  let normalizedCommands: ValidationCommandSpec[];

  try {
    normalizedCommands = options.commands.map(validateCommandSpec);
  } catch (error) {
    const message = error instanceof Error ? error.message : String(error);
    const invalidCommand = recordInvalidCommand(options.commands, message, artifactFindingId);
    commands.push(invalidCommand);

    await writeFile(join(options.outputDir, invalidCommand.stdoutPath), "");
    await writeFile(join(options.outputDir, invalidCommand.stderrPath), truncateOutput(message));
    await writeJson(join(validationDir, "commands.json"), commands);

    return {
      findingId: options.findingId,
      status: "failed",
      commands,
      changedFiles: [],
      diffSummary: summarizeValidation(commands)
    };
  }

  for (const [index, commandSpec] of normalizedCommands.entries()) {
    const { command, args } = commandSpec;
    const renderedCommand = renderCommand({ command, args });
    const result = await runner(command, args, {
      cwd: options.repoPath,
      env: validationEnvironment(),
      replaceEnv: true,
      timeoutMs: validationTimeoutMs,
      maxOutputBytes: validationOutputLimitBytes
    });
    const stdoutPath = `validation/${artifactFindingId}/stdout-${index}.log`;
    const stderrPath = `validation/${artifactFindingId}/stderr-${index}.log`;

    await writeFile(join(options.outputDir, stdoutPath), truncateOutput(result.stdout));
    await writeFile(join(options.outputDir, stderrPath), truncateOutput(result.stderr));

    commands.push({
      command: renderedCommand,
      exitCode: result.exitCode,
      stdoutPath,
      stderrPath
    });
  }

  await writeJson(join(validationDir, "commands.json"), commands);

  return {
    findingId: options.findingId,
    status: validationStatus(commands),
    commands,
    changedFiles: [],
    diffSummary: summarizeValidation(commands)
  };
}

function validateCommandSpec(commandSpec: unknown): ValidationCommandSpec {
  if (
    typeof commandSpec !== "object" ||
    commandSpec === null ||
    Array.isArray(commandSpec) ||
    typeof (commandSpec as { command?: unknown }).command !== "string" ||
    !Array.isArray((commandSpec as { args?: unknown }).args)
  ) {
    throw new Error("Validation command must use structured argv");
  }

  const command = (commandSpec as { command: string }).command.trim();
  const args = (commandSpec as { args: unknown[] }).args;
  if (command.length === 0) {
    throw new Error("Validation command must not be empty");
  }
  if (command.includes("/") || command.includes("\\") || shellMetacharacterPattern.test(command)) {
    throw new Error("Validation command must be a bare executable name");
  }
  if (!allowedValidationCommands.has(command)) {
    throw new Error(`Validation command is not allowed: ${command}`);
  }

  const normalizedArgs = args.map((arg) => {
    if (typeof arg !== "string") {
      throw new Error("Validation command arguments must be strings");
    }
    if (shellMetacharacterPattern.test(arg)) {
      throw new Error("Validation command argument contains shell metacharacters");
    }
    return arg;
  });

  return {
    command,
    args: normalizedArgs
  };
}

function renderCommand(commandSpec: ValidationCommandSpec): string {
  const needsStructured = commandSpec.args.some((arg) => arg.includes(" ") || arg === "");
  if (needsStructured) {
    return `${commandSpec.command} ${JSON.stringify(commandSpec.args)}`;
  }
  return [commandSpec.command, ...commandSpec.args].join(" ");
}

function recordInvalidCommand(
  commandSpecs: unknown[],
  message: string,
  artifactFindingId: string
): RecordedCommand {
  const firstInvalidCommand = commandSpecs.find((commandSpec) => {
    try {
      validateCommandSpec(commandSpec);
      return false;
    } catch {
      return true;
    }
  });

  return {
    command: renderInvalidCommand(firstInvalidCommand),
    exitCode: 125,
    stdoutPath: `validation/${artifactFindingId}/stdout-0.log`,
    stderrPath: `validation/${artifactFindingId}/stderr-0.log`,
    error: message
  };
}

function renderInvalidCommand(commandSpec: unknown): string {
  if (typeof commandSpec === "string" && commandSpec.trim() !== "") {
    return commandSpec.trim();
  }

  if (typeof commandSpec === "object" && commandSpec !== null && !Array.isArray(commandSpec)) {
    const command = (commandSpec as { command?: unknown }).command;
    const args = (commandSpec as { args?: unknown }).args;
    if (typeof command === "string" && command.trim() !== "") {
      const renderedArgs = Array.isArray(args) ? args.filter((arg): arg is string => typeof arg === "string") : [];
      return renderCommand({ command: command.trim(), args: renderedArgs });
    }
  }

  return "invalid validation command";
}

function validationEnvironment(): NodeJS.ProcessEnv {
  const env: NodeJS.ProcessEnv = {};
  for (const key of ["PATH", "HOME", "LANG", "LC_ALL", "CI"]) {
    const value = process.env[key];
    if (value !== undefined) {
      env[key] = value;
    }
  }

  env.CI = env.CI ?? "1";
  return env;
}

function truncateOutput(text: string): string {
  return truncateUtf8(text, validationOutputLimitBytes);
}

function validationStatus(commands: ValidationCommand[]): ValidationResult["status"] {
  if (commands.length === 0) {
    return "not_run";
  }

  return commands.every((command) => command.exitCode === 0) ? "passed" : "failed";
}

function summarizeValidation(commands: RecordedCommand[]): string {
  if (commands.length === 0) {
    return "No validation commands were run.";
  }

  return commands
    .map((command) => {
      const summary = `${command.command}: exit ${command.exitCode}`;
      return command.error === undefined ? summary : `${summary}\n${command.error}`;
    })
    .join("\n");
}

async function writeJson(filePath: string, value: unknown): Promise<void> {
  const json = JSON.stringify(value, null, 2);
  if (json === undefined) {
    throw new TypeError("JSON file value must be JSON-serializable");
  }
  await writeFile(filePath, `${json}\n`);
}
