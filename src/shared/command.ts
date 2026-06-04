import { spawn } from "node:child_process";

export interface CommandResult {
  exitCode: number;
  stdout: string;
  stderr: string;
}

export type CommandRunner = (
  command: string,
  args: string[],
  options?: {
    cwd?: string;
    env?: NodeJS.ProcessEnv;
    timeoutMs?: number;
    maxOutputBytes?: number;
    replaceEnv?: boolean;
  }
) => Promise<CommandResult>;

const sigtermGraceMs = 5000;
const sigkillGraceMs = 5000;

export const runCommand: CommandRunner = (command, args, options = {}) =>
  new Promise((resolve) => {
    const child = spawn(command, args, {
      cwd: options.cwd,
      env: options.replaceEnv ? options.env : { ...process.env, ...options.env },
      stdio: ["ignore", "pipe", "pipe"]
    });

    let stdout = "";
    let stderr = "";
    let settled = false;
    let timedOut = false;
    const maxOutputBytes = options.maxOutputBytes ?? Number.POSITIVE_INFINITY;
    const timeoutMessage =
      options.timeoutMs === undefined ? "" : `Command timed out after ${options.timeoutMs}ms`;

    const onStdoutData = (chunk: Buffer | string) => {
      stdout = appendLimited(stdout, String(chunk), maxOutputBytes);
    };
    const onStderrData = (chunk: Buffer | string) => {
      stderr = appendLimited(stderr, String(chunk), maxOutputBytes);
    };
    const onError = (error: Error) => {
      settle({ exitCode: 127, stdout, stderr: error.message });
    };
    const onClose = (exitCode: number | null) => {
      settle({
        exitCode: timedOut ? 124 : (exitCode ?? 1),
        stdout,
        stderr: timedOut ? appendLimited(stderr, timeoutMessage, maxOutputBytes) : stderr
      });
    };

    const cleanup = () => {
      clearTimeout(timeout);
      clearTimeout(killTimeout);
      child.stdout?.off("data", onStdoutData);
      child.stderr?.off("data", onStderrData);
      child.off("error", onError);
      child.off("close", onClose);
    };

    const settle = (result: CommandResult) => {
      if (!settled) {
        settled = true;
        cleanup();
        resolve(result);
      }
    };

    let timeout: NodeJS.Timeout | undefined;
    let killTimeout: NodeJS.Timeout | undefined;

    if (options.timeoutMs !== undefined) {
      timeout = setTimeout(() => {
        if (!settled) {
          timedOut = true;
          child.kill("SIGTERM");
          killTimeout = setTimeout(() => {
            if (!settled) {
              child.kill("SIGKILL");
              killTimeout = setTimeout(() => {
                settle({
                  exitCode: 124,
                  stdout,
                  stderr: appendLimited(stderr, `${timeoutMessage} (SIGKILL also failed)`, maxOutputBytes)
                });
              }, sigkillGraceMs);
            }
          }, sigtermGraceMs);
        }
      }, options.timeoutMs);
    }

    child.stdout?.setEncoding("utf8");
    child.stderr?.setEncoding("utf8");
    child.stdout?.on("data", onStdoutData);
    child.stderr?.on("data", onStderrData);
    child.on("error", onError);
    child.on("close", onClose);
  });

function appendLimited(current: string, chunk: string, maxBytes: number): string {
  if (!Number.isFinite(maxBytes)) {
    return current + chunk;
  }

  const currentBytes = Buffer.byteLength(current, "utf8");
  const remainingBytes = maxBytes - currentBytes;
  if (remainingBytes <= 0) {
    if (current.endsWith("[truncated]")) {
      return current;
    }
    const marker = "[truncated]";
    const markerBytes = Buffer.byteLength(marker, "utf8");
    if (currentBytes + markerBytes <= maxBytes) {
      return current + marker;
    }
    const trimTo = Math.max(0, maxBytes - markerBytes);
    if (trimTo > 0) {
      return truncateUtf8(current, trimTo) + marker;
    }
    return current;
  }

  const chunkBytes = Buffer.byteLength(chunk, "utf8");
  if (chunkBytes <= remainingBytes) {
    return current + chunk;
  }

  const marker = "[truncated]";
  const markerBytes = Buffer.byteLength(marker, "utf8");
  const availableForChunk = Math.max(0, remainingBytes - markerBytes);
  let truncatedChunk = "";
  if (availableForChunk > 0) {
    truncatedChunk = truncateUtf8(chunk, availableForChunk);
  }
  return current + truncatedChunk + marker;
}

export function truncateUtf8(text: string, maxBytes: number): string {
  const buffer = Buffer.from(text, "utf8");
  if (buffer.length <= maxBytes) {
    return text;
  }
  let end = maxBytes;
  while (end > 0 && (buffer[end] & 0xc0) === 0x80) {
    end -= 1;
  }
  return buffer.subarray(0, end).toString("utf8");
}
