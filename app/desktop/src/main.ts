import { invoke } from "@tauri-apps/api/core";
import { getCurrentWebviewWindow } from "@tauri-apps/api/webviewWindow";
import { open, save } from "@tauri-apps/plugin-dialog";
import { hydrateIcons, icon } from "./icons";
import { renderMarkdown } from "./markdown";
import "./styles.css";

// ---- Types mirroring the Rust JobUpdate / FormatInfo payloads ----

type JobStatus = "queued" | "converting" | "done" | "failed";
type EngineChoice = "auto" | "rust" | "python";

interface JobUpdate {
  id: string;
  path: string;
  status: JobStatus;
  size?: number | null;
  markdown?: string | null;
  title?: string | null;
  error?: string | null;
  degraded?: boolean;
  duration_ms?: number | null;
}

interface FormatInfo {
  name: string;
  extensions: string[];
  notes: string;
}

interface Capabilities {
  python_engine: boolean;
  llm_captions: boolean;
}

interface Job {
  id: string;
  path: string;
  name: string;
  size: number;
  status: JobStatus;
  markdown: string | null;
  title: string | null;
  error: string | null;
  degraded: boolean;
  /** Backend wall-clock conversion time; frozen on done/failed. */
  durationMs: number | null;
  /** Client timestamp (ms) when this job entered the converting state. */
  startedAt: number | null;
  /** Engine used for this job, so Retry re-invokes with the same choice. */
  engine: EngineChoice;
  /** True once the user has edited the raw markdown in the preview. */
  edited: boolean;
}

type Filter = "all" | "done" | "failed";

// ---- State ----

const jobs = new Map<string, Job>();
let selectedId: string | null = null;
let viewMode: "rendered" | "raw" = "rendered";
let engine: EngineChoice = "auto";
let activeTab: "queue" | "logs" = "queue";
let filter: Filter = "all";
/** Single ticker that refreshes elapsed times while ≥1 job is converting. */
let ticker: number | null = null;

// ---- DOM refs ----

const $ = <T extends HTMLElement>(id: string) => document.getElementById(id) as T;
const queueEl = $("queue");
const previewEl = $("preview");
const previewTitleEl = $("preview-title");
const copyBtn = $<HTMLButtonElement>("copy-btn");
const saveBtn = $<HTMLButtonElement>("save-btn");
const viewRenderedBtn = $<HTMLButtonElement>("view-rendered");
const viewRawBtn = $<HTMLButtonElement>("view-raw");
const themeBtn = $<HTMLButtonElement>("theme-btn");
const dropzone = $("dropzone");
const engineSelect = $<HTMLSelectElement>("engine-select");
const urlForm = $<HTMLFormElement>("url-form");
const urlInput = $<HTMLInputElement>("url-input");
const tabQueueBtn = $<HTMLButtonElement>("tab-queue");
const tabLogsBtn = $<HTMLButtonElement>("tab-logs");
const viewQueueEl = $("view-queue");
const viewLogsEl = $("view-logs");
const logsEl = $("logs");
const logsCopyBtn = $<HTMLButtonElement>("logs-copy");
const logsClearBtn = $<HTMLButtonElement>("logs-clear");
const batchProgressEl = $("batch-progress");
const batchProgressText = $("batch-progress-text");
const batchProgressFill = $("batch-progress-fill");
const filterBtns: Record<Filter, HTMLButtonElement> = {
  all: $<HTMLButtonElement>("filter-all"),
  done: $<HTMLButtonElement>("filter-done"),
  failed: $<HTMLButtonElement>("filter-failed"),
};
const countEls: Record<Filter, HTMLElement> = {
  all: $("count-all"),
  done: $("count-done"),
  failed: $("count-failed"),
};

// ---- Helpers ----

function baseName(p: string): string {
  return p.split(/[\\/]/).pop() || p;
}

function fmtSize(bytes: number): string {
  if (!bytes) return "—";
  const units = ["B", "KB", "MB", "GB"];
  let n = bytes;
  let u = 0;
  while (n >= 1024 && u < units.length - 1) {
    n /= 1024;
    u++;
  }
  return `${n >= 10 || u === 0 ? Math.round(n) : n.toFixed(1)} ${units[u]}`;
}

/** Human-friendly duration: "830ms", "1.3s", or "2m 05s". */
function formatDuration(ms: number): string {
  if (ms < 1000) return `${Math.round(ms)}ms`;
  const secs = ms / 1000;
  if (secs < 60) return `${secs.toFixed(secs < 10 ? 1 : 0)}s`;
  const m = Math.floor(secs / 60);
  const s = Math.round(secs % 60);
  return `${m}m ${String(s).padStart(2, "0")}s`;
}

// ---- Logs (persisted to localStorage, capped at 500 lines) ----

const LOG_CAP = 500;
const LOG_KEY = "logs";
type LogLevel = "info" | "ok" | "warn" | "err";
interface LogLine {
  t: string; // HH:MM:SS
  level: LogLevel;
  msg: string;
}
let logLines: LogLine[] = [];

function loadLogs(): void {
  try {
    const raw = localStorage.getItem(LOG_KEY);
    if (!raw) return;
    const parsed = JSON.parse(raw);
    if (Array.isArray(parsed)) {
      logLines = parsed
        .filter((l) => l && typeof l.t === "string" && typeof l.msg === "string")
        .slice(-LOG_CAP)
        .map((l) => ({
          t: l.t,
          level: ["info", "ok", "warn", "err"].includes(l.level) ? l.level : "info",
          msg: l.msg,
        }));
    }
  } catch {
    logLines = [];
  }
}

function persistLogs(): void {
  try {
    localStorage.setItem(LOG_KEY, JSON.stringify(logLines));
  } catch {
    /* quota / unavailable — logs are best-effort */
  }
}

function timestamp(): string {
  const d = new Date();
  const p = (n: number) => String(n).padStart(2, "0");
  return `${p(d.getHours())}:${p(d.getMinutes())}:${p(d.getSeconds())}`;
}

/** Is the logs panel scrolled (near) to the bottom? */
function logsAtBottom(): boolean {
  return logsEl.scrollHeight - logsEl.scrollTop - logsEl.clientHeight < 24;
}

function log(level: LogLevel, msg: string): void {
  const line: LogLine = { t: timestamp(), level, msg };
  logLines.push(line);
  if (logLines.length > LOG_CAP) logLines = logLines.slice(-LOG_CAP);
  persistLogs();
  const stick = logsAtBottom();
  logsEl.appendChild(renderLogLine(line));
  // Keep DOM bounded too.
  while (logsEl.childElementCount > LOG_CAP) logsEl.removeChild(logsEl.firstChild!);
  if (stick) logsEl.scrollTop = logsEl.scrollHeight;
}

function renderLogLine(line: LogLine): HTMLElement {
  const div = document.createElement("div");
  div.className = `log-line log-${line.level}`;
  const t = document.createElement("span");
  t.className = "log-time";
  t.textContent = line.t;
  const lvl = document.createElement("span");
  lvl.className = "log-level";
  lvl.textContent = line.level.toUpperCase();
  const m = document.createElement("span");
  m.className = "log-msg";
  m.textContent = line.msg;
  div.append(t, lvl, m);
  return div;
}

function renderLogs(): void {
  const frag = document.createDocumentFragment();
  for (const line of logLines) frag.appendChild(renderLogLine(line));
  logsEl.replaceChildren(frag);
  logsEl.scrollTop = logsEl.scrollHeight;
}

const STATUS_ICON: Record<JobStatus, string> = {
  queued: "clock",
  converting: "loader-circle",
  done: "circle-check",
  failed: "circle-x",
};

const STATUS_LABEL: Record<JobStatus, string> = {
  queued: "Queued",
  converting: "Converting…",
  done: "Done",
  failed: "Failed",
};

// ---- Queue rendering ----

/** Elapsed/finished time text for a job's meta line. */
function durationText(job: Job): string {
  if (job.status === "converting" && job.startedAt != null) {
    return formatDuration(Date.now() - job.startedAt);
  }
  if (job.durationMs != null) return formatDuration(job.durationMs);
  return "";
}

function jobMatchesFilter(job: Job): boolean {
  if (filter === "done") return job.status === "done";
  if (filter === "failed") return job.status === "failed";
  return true;
}

function renderQueue(): void {
  updateCounts();
  updateBatchProgress();
  if (jobs.size === 0) {
    queueEl.replaceChildren();
    return;
  }
  const frag = document.createDocumentFragment();
  let shown = 0;
  for (const job of jobs.values()) {
    if (!jobMatchesFilter(job)) continue;
    shown++;
    const li = document.createElement("li");
    li.className = "job" + (job.id === selectedId ? " selected" : "");
    li.dataset.id = job.id;
    li.dataset.status = job.status;
    if (job.status === "done") li.classList.add("clickable");

    const spinning = job.status === "converting" ? " spin" : "";
    const degradedBadge =
      job.status === "done" && job.degraded
        ? `<span class="job-degraded" title="Partial fidelity — configure the Python engine for OCR/transcription">${icon(
            "triangle-alert",
          )}</span>`
        : "";
    const dur = durationText(job);
    const editedBadge = job.edited
      ? `<span class="job-edited" title="Edited">●</span>`
      : "";
    const errPart = job.error
      ? ` · <span class="job-err" title="${escapeHtml(job.error)}">${escapeHtml(
          job.error,
        )}</span>`
      : "";
    const progress =
      job.status === "converting"
        ? `<div class="job-progress" role="progressbar" aria-label="Converting"><div class="job-progress-bar"></div></div>`
        : "";

    const actions: string[] = [];
    if (job.status === "done") {
      actions.push(
        `<button class="job-act" data-act="preview" title="Preview" aria-label="Preview ${escapeHtml(
          job.name,
        )}">${icon("eye")}</button>`,
      );
    }
    if (job.status === "done" || job.status === "failed") {
      actions.push(
        `<button class="job-act" data-act="retry" title="Retry" aria-label="Retry ${escapeHtml(
          job.name,
        )}">${icon("rotate-cw")}</button>`,
      );
    }

    li.innerHTML = `
      <span class="job-status status-${job.status}">${icon(STATUS_ICON[job.status], spinning)}</span>
      <span class="job-info">
        <span class="job-name" title="${escapeHtml(job.path)}">${escapeHtml(job.name)}${editedBadge}</span>
        <span class="job-meta">${fmtSize(job.size)} · ${STATUS_LABEL[job.status]}${
          dur ? " · " + dur : ""
        }${errPart}</span>
        ${progress}
      </span>${degradedBadge}<span class="job-actions">${actions.join("")}</span>`;
    frag.appendChild(li);
  }
  queueEl.replaceChildren(frag);
  if (shown === 0) {
    const empty = document.createElement("li");
    empty.className = "queue-empty";
    empty.textContent =
      filter === "all" ? "No jobs yet." : `No ${filter} jobs.`;
    queueEl.appendChild(empty);
  }
}

function updateCounts(): void {
  let done = 0;
  let failed = 0;
  for (const job of jobs.values()) {
    if (job.status === "done") done++;
    else if (job.status === "failed") failed++;
  }
  countEls.all.textContent = String(jobs.size);
  countEls.done.textContent = String(done);
  countEls.failed.textContent = String(failed);
}

/** Determinate batch bar: (done+failed)/total, shown only while active. */
function updateBatchProgress(): void {
  let total = 0;
  let finished = 0;
  let active = 0;
  for (const job of jobs.values()) {
    total++;
    if (job.status === "done" || job.status === "failed") finished++;
    else active++;
  }
  if (active === 0 || total === 0) {
    batchProgressEl.hidden = true;
    batchProgressEl.setAttribute("aria-hidden", "true");
    return;
  }
  batchProgressEl.hidden = false;
  batchProgressEl.setAttribute("aria-hidden", "false");
  const pct = total ? Math.round((finished / total) * 100) : 0;
  batchProgressFill.style.width = `${pct}%`;
  batchProgressText.textContent = `${finished} / ${total} converted`;
}

function setFilter(f: Filter): void {
  filter = f;
  for (const key of Object.keys(filterBtns) as Filter[]) {
    const on = key === f;
    filterBtns[key].classList.toggle("active", on);
    filterBtns[key].setAttribute("aria-selected", on ? "true" : "false");
  }
  localStorage.setItem("filter", f);
  renderQueue();
}

// ---- Elapsed-time ticker (single interval while any job converts) ----

function anyConverting(): boolean {
  for (const job of jobs.values()) {
    if (job.status === "converting" || job.status === "queued") return true;
  }
  return false;
}

function syncTicker(): void {
  if (anyConverting()) {
    if (ticker == null) {
      ticker = window.setInterval(() => {
        // Only repaint converting rows' meta — cheap full re-render is fine
        // given the queue is small, but guard against the logs tab.
        for (const job of jobs.values()) {
          if (job.status !== "converting") continue;
          const row = queueEl.querySelector<HTMLElement>(
            `.job[data-id="${CSS.escape(job.id)}"] .job-meta`,
          );
          if (row) {
            const dur = durationText(job);
            row.textContent = `${fmtSize(job.size)} · ${STATUS_LABEL[job.status]}${
              dur ? " · " + dur : ""
            }`;
          }
        }
      }, 200);
    }
  } else if (ticker != null) {
    window.clearInterval(ticker);
    ticker = null;
  }
}

function escapeHtml(s: string): string {
  return s.replace(/[&<>"]/g, (c) =>
    c === "&" ? "&amp;" : c === "<" ? "&lt;" : c === ">" ? "&gt;" : "&quot;",
  );
}

// ---- Preview ----

function selectJob(id: string): void {
  const job = jobs.get(id);
  if (!job || job.status !== "done") return;
  selectedId = id;
  renderQueue();
  renderPreview();
}

function renderPreview(): void {
  const job = selectedId ? jobs.get(selectedId) : null;
  if (!job || job.markdown == null) {
    previewTitleEl.textContent = "Preview";
    previewTitleEl.classList.remove("is-edited");
    previewEl.innerHTML = `<div class="preview-empty">Select a finished job to preview its Markdown.</div>`;
    copyBtn.disabled = true;
    saveBtn.disabled = true;
    return;
  }
  previewTitleEl.textContent = job.title || job.name;
  previewTitleEl.classList.toggle("is-edited", job.edited);
  if (job.edited) previewTitleEl.title = "Edited (unsaved changes)";
  else previewTitleEl.removeAttribute("title");
  copyBtn.disabled = false;
  saveBtn.disabled = false;
  if (viewMode === "rendered") {
    previewEl.innerHTML = `<article class="md">${renderMarkdown(job.markdown)}</article>`;
  } else {
    // Raw view is an editable textarea; edits update the job's markdown.
    const ta = document.createElement("textarea");
    ta.className = "raw raw-edit";
    ta.spellcheck = false;
    ta.value = job.markdown;
    ta.setAttribute("aria-label", "Editable Markdown source");
    ta.addEventListener("input", () => {
      const j = jobs.get(job.id);
      if (!j) return;
      j.markdown = ta.value;
      if (!j.edited) {
        j.edited = true;
        previewTitleEl.classList.add("is-edited");
        previewTitleEl.title = "Edited (unsaved changes)";
        log("info", `Edited ${j.name}`);
        renderQueue();
      }
    });
    previewEl.replaceChildren(ta);
  }
}

function setViewMode(mode: "rendered" | "raw"): void {
  viewMode = mode;
  viewRenderedBtn.classList.toggle("active", mode === "rendered");
  viewRawBtn.classList.toggle("active", mode === "raw");
  renderPreview();
}

// ---- Conversion ----

let counter = 0;
async function enqueue(paths: string[]): Promise<void> {
  if (!paths.length) return;
  const requests = paths.map((path) => {
    const id = `job-${Date.now()}-${counter++}`;
    const name = jobName(path);
    jobs.set(id, {
      id,
      path,
      name,
      size: 0,
      status: "queued",
      markdown: null,
      title: null,
      error: null,
      degraded: false,
      durationMs: null,
      startedAt: null,
      engine,
      edited: false,
    });
    log("info", `Queued ${name} (engine: ${engine})`);
    return { id, path, engine };
  });
  renderQueue();
  syncTicker();
  try {
    await invoke("convert_files", { requests });
  } catch (e) {
    console.error("convert_files failed", e);
    log("err", `convert_files failed: ${String(e)}`);
  }
}

/** Re-run a single job in place, reusing its id, path and engine choice. */
async function retry(id: string): Promise<void> {
  const job = jobs.get(id);
  if (!job) return;
  job.status = "queued";
  job.markdown = null;
  job.title = null;
  job.error = null;
  job.degraded = false;
  job.durationMs = null;
  job.startedAt = null;
  job.edited = false;
  if (selectedId === id) {
    selectedId = null;
    renderPreview();
  }
  log("info", `Retrying ${job.name} (engine: ${job.engine})`);
  renderQueue();
  syncTicker();
  try {
    await invoke("convert_files", {
      requests: [{ id: job.id, path: job.path, engine: job.engine }],
    });
  } catch (e) {
    console.error("convert_files (retry) failed", e);
    log("err", `retry failed: ${String(e)}`);
  }
}

function isHttpUrl(value: string): boolean {
  return /^https?:\/\//i.test(value.trim());
}

/** Display name for a queue entry: last path segment, or the URL itself. */
function jobName(src: string): string {
  if (isHttpUrl(src)) {
    try {
      const u = new URL(src);
      const last = u.pathname.split("/").filter(Boolean).pop();
      return last || u.hostname;
    } catch {
      return src;
    }
  }
  return baseName(src);
}

function applyUpdate(u: JobUpdate): void {
  const job = jobs.get(u.id);
  if (!job) return;
  const prev = job.status;
  job.status = u.status;
  if (u.size != null) job.size = u.size;
  if (u.markdown != null) job.markdown = u.markdown;
  if (u.title != null) job.title = u.title;
  if (u.error != null) job.error = u.error;
  if (u.status === "done") job.degraded = u.degraded === true;
  if (u.status === "converting") {
    job.startedAt = Date.now();
  }
  if (u.status === "done" || u.status === "failed") {
    if (u.duration_ms != null) job.durationMs = u.duration_ms;
    job.startedAt = null;
  }
  // Log lifecycle transitions once per real change.
  if (prev !== u.status) {
    const dur = job.durationMs != null ? ` in ${formatDuration(job.durationMs)}` : "";
    if (u.status === "converting") log("info", `Converting ${job.name}…`);
    else if (u.status === "done")
      log("ok", `Done ${job.name}${dur}${job.degraded ? " (degraded)" : ""}`);
    else if (u.status === "failed")
      log("err", `Failed ${job.name}${dur}: ${job.error ?? "unknown error"}`);
  }
  renderQueue();
  syncTicker();
  if (job.id === selectedId) renderPreview();
}

// ---- Theme ----

function applyTheme(theme: "dark" | "light"): void {
  document.documentElement.dataset.theme = theme;
  const ico = themeBtn.querySelector(".ico") as HTMLElement;
  ico.innerHTML = icon(theme === "dark" ? "sun" : "moon");
  localStorage.setItem("theme", theme);
}

function initTheme(): void {
  const stored = localStorage.getItem("theme") as "dark" | "light" | null;
  const prefersDark =
    window.matchMedia && window.matchMedia("(prefers-color-scheme: dark)").matches;
  applyTheme(stored ?? (prefersDark ? "dark" : "light"));
}

// ---- Engine selection ----

function initEngine(): void {
  const stored = localStorage.getItem("engine");
  if (stored === "auto" || stored === "rust" || stored === "python") {
    engine = stored;
  }
  engineSelect.value = engine;
}

function setEngine(value: string): void {
  engine = value === "rust" || value === "python" ? value : "auto";
  engineSelect.value = engine;
  localStorage.setItem("engine", engine);
}

// ---- Sidebar tab (Queue / Logs) ----

function setTab(tab: "queue" | "logs"): void {
  activeTab = tab;
  const queueOn = tab === "queue";
  tabQueueBtn.classList.toggle("active", queueOn);
  tabLogsBtn.classList.toggle("active", !queueOn);
  tabQueueBtn.setAttribute("aria-selected", queueOn ? "true" : "false");
  tabLogsBtn.setAttribute("aria-selected", !queueOn ? "true" : "false");
  viewQueueEl.hidden = !queueOn;
  viewLogsEl.hidden = queueOn;
  localStorage.setItem("activeTab", tab);
  if (tab === "logs") logsEl.scrollTop = logsEl.scrollHeight;
}

function initTab(): void {
  const stored = localStorage.getItem("activeTab");
  setTab(stored === "logs" ? "logs" : "queue");
}

function initFilter(): void {
  const stored = localStorage.getItem("filter");
  setFilter(stored === "done" || stored === "failed" ? stored : "all");
}

// ---- Footer formats & capabilities ----

async function loadFormats(): Promise<void> {
  try {
    const formats = await invoke<FormatInfo[]>("list_supported");
    const exts = new Set<string>();
    for (const f of formats) for (const e of f.extensions) exts.add(e.replace(/^\./, ""));
    $("formats").textContent = [...exts].join("  ");
    log("info", `Loaded ${formats.length} supported formats`);
  } catch (e) {
    console.error("list_supported failed", e);
    log("err", `list_supported failed: ${String(e)}`);
  }
}

async function loadCapabilities(): Promise<void> {
  try {
    const caps = await invoke<Capabilities>("get_capabilities");
    setCap(
      "cap-python",
      caps.python_engine,
      caps.python_engine
        ? "Python engine available"
        : "Python engine not configured — set MARKITDOWN_PY_BIN to a markitdown binary",
    );
    setCap(
      "cap-llm",
      caps.llm_captions,
      caps.llm_captions
        ? "LLM image captions available"
        : "LLM captions not configured — set MARKITDOWN_LLM_API_KEY and MARKITDOWN_LLM_MODEL",
    );
    log(
      "info",
      `Capabilities — Python engine: ${caps.python_engine ? "on" : "off"}, LLM captions: ${
        caps.llm_captions ? "on" : "off"
      }`,
    );
  } catch (e) {
    console.error("get_capabilities failed", e);
    log("err", `get_capabilities failed: ${String(e)}`);
  }
}

function setCap(id: string, on: boolean, tooltip: string): void {
  const el = $(id);
  el.dataset.on = on ? "true" : "false";
  el.title = tooltip;
}

// ---- Wire up events ----

async function browseForFiles(): Promise<void> {
  const selection = await open({ multiple: true, directory: false });
  if (!selection) return;
  await enqueue(Array.isArray(selection) ? selection : [selection]);
}

function init(): void {
  hydrateIcons();
  loadLogs();
  renderLogs();
  initTheme();
  initEngine();
  initTab();
  initFilter();
  loadFormats();
  loadCapabilities();

  themeBtn.addEventListener("click", () => {
    applyTheme(document.documentElement.dataset.theme === "dark" ? "light" : "dark");
  });

  engineSelect.addEventListener("change", () => setEngine(engineSelect.value));

  // Sidebar tabs
  tabQueueBtn.addEventListener("click", () => setTab("queue"));
  tabLogsBtn.addEventListener("click", () => setTab("logs"));

  // Filter pills
  for (const key of Object.keys(filterBtns) as Filter[]) {
    filterBtns[key].addEventListener("click", () => setFilter(key));
  }

  // Logs toolbar
  logsCopyBtn.addEventListener("click", async () => {
    const text = logLines.map((l) => `${l.t} ${l.level.toUpperCase()} ${l.msg}`).join("\n");
    await navigator.clipboard.writeText(text);
    flash(logsCopyBtn);
  });
  logsClearBtn.addEventListener("click", () => {
    logLines = [];
    persistLogs();
    renderLogs();
  });

  // Clickable, keyboard-accessible dropzone (same picker as Add files).
  dropzone.addEventListener("click", () => {
    void browseForFiles();
  });
  dropzone.addEventListener("keydown", (e) => {
    if (e.key === "Enter" || e.key === " ") {
      e.preventDefault();
      void browseForFiles();
    }
  });

  urlForm.addEventListener("submit", (e) => {
    e.preventDefault();
    const value = urlInput.value.trim();
    if (!isHttpUrl(value)) {
      urlInput.classList.add("invalid");
      setTimeout(() => urlInput.classList.remove("invalid"), 600);
      return;
    }
    urlInput.value = "";
    enqueue([value]);
  });

  $("browse-btn").addEventListener("click", () => {
    void browseForFiles();
  });

  queueEl.addEventListener("click", (e) => {
    const target = e.target as HTMLElement;
    const li = target.closest<HTMLElement>(".job");
    if (!li?.dataset.id) return;
    const actBtn = target.closest<HTMLElement>(".job-act");
    if (actBtn) {
      e.stopPropagation();
      if (actBtn.dataset.act === "retry") void retry(li.dataset.id);
      else if (actBtn.dataset.act === "preview") selectJob(li.dataset.id);
      return;
    }
    selectJob(li.dataset.id);
  });

  viewRenderedBtn.addEventListener("click", () => setViewMode("rendered"));
  viewRawBtn.addEventListener("click", () => setViewMode("raw"));

  copyBtn.addEventListener("click", async () => {
    const job = selectedId ? jobs.get(selectedId) : null;
    if (job?.markdown != null) {
      await navigator.clipboard.writeText(job.markdown);
      flash(copyBtn);
    }
  });

  saveBtn.addEventListener("click", async () => {
    const job = selectedId ? jobs.get(selectedId) : null;
    if (job?.markdown == null) return;
    const suggested = job.name.replace(/\.[^.]+$/, "") + ".md";
    const target = await save({
      defaultPath: suggested,
      filters: [{ name: "Markdown", extensions: ["md"] }],
    });
    if (!target) return;
    try {
      await invoke("save_markdown", { path: target, contents: job.markdown });
      job.edited = false;
      previewTitleEl.classList.remove("is-edited");
      previewTitleEl.removeAttribute("title");
      renderQueue();
      log("ok", `Saved ${job.name} → ${baseName(target)}`);
      flash(saveBtn);
    } catch (err) {
      console.error("save_markdown failed", err);
      log("err", `save_markdown failed: ${String(err)}`);
    }
  });

  // Native Tauri drag & drop gives real filesystem paths.
  const webview = getCurrentWebviewWindow();
  webview.onDragDropEvent((event) => {
    const { type } = event.payload;
    if (type === "enter" || type === "over") {
      dropzone.classList.add("dragover");
    } else if (type === "drop") {
      dropzone.classList.remove("dragover");
      if (activeTab !== "queue") setTab("queue");
      enqueue(event.payload.paths);
    } else {
      dropzone.classList.remove("dragover");
    }
  });
}

function flash(btn: HTMLButtonElement): void {
  btn.classList.add("flash");
  setTimeout(() => btn.classList.remove("flash"), 600);
}

// Listen for per-job updates emitted from Rust.
getCurrentWebviewWindow().listen<JobUpdate>("job:update", (e) => applyUpdate(e.payload));

if (document.readyState === "loading") {
  document.addEventListener("DOMContentLoaded", init);
} else {
  init();
}
