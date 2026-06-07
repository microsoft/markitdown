# MarkItDown Desktop

A lightweight cross-platform desktop UI for **MarkItDown**, the pure-Rust
file→Markdown converter. Drop files in, watch a live job queue convert them on
background threads, and preview / copy / save the resulting Markdown.

Built with **Tauri 2** + **vanilla TypeScript** (no UI framework). The
conversion engine (`markitdown-core`) runs **in-process** — no shelling out.

## Features

- Drag-and-drop zone (native OS file drop → real paths) + "Add files" dialog.
- Job queue with per-file name, size, and live status (queued / converting /
  done / failed), each with a Lucide status icon.
- Click a finished job to preview its Markdown, with a **Rendered / Raw** toggle
  (rendered via a tiny dependency-free Markdown renderer).
- Copy-to-clipboard and Save-as `.md`.
- Dark / light theme toggle, persisted in `localStorage`.
- Footer listing supported input formats (queried from the engine).
- Many files can be dropped at once; conversions run on bounded background
  threads and never block the UI thread.

## Prerequisites

- **Rust** (stable) + Cargo — https://rustup.rs
- **Node.js** 18+ and npm
- OS webview / build dependencies for Tauri 2:
  - **macOS**: Xcode Command Line Tools (`xcode-select --install`).
  - **Windows**: WebView2 runtime (preinstalled on Win 11) + MSVC build tools.
  - **Linux**: `webkit2gtk-4.1`, `libayatana-appindicator3`, `librsvg2`,
    `build-essential` (see the Tauri prerequisites guide).

## Develop

```sh
npm install
npm run tauri dev
```

`tauri dev` starts Vite on http://localhost:1420 and launches the native
window. (The frontend alone can be previewed with `npm run dev`, but the
`invoke`/event backend is only available inside the Tauri shell.)

## Build a release bundle

```sh
npm install
npm run tauri build
```

Produces a platform installer (`.dmg`/`.app`, `.msi`/`.exe`, `.deb`/`.AppImage`)
under `src-tauri/target/release/bundle/`.

## Tests & checks

```sh
# Frontend type-check + production build
npm run build

# Rust backend (run from src-tauri)
cd src-tauri
cargo check
cargo test
```

## Architecture

```
            ┌────────────────────────────────────────────┐
            │  Frontend  (Vite + vanilla TS, ~38 KB)       │
            │   index.html · main.ts · markdown.ts ·       │
            │   icons.ts (inlined Lucide SVGs) · styles.css│
            └───────────────┬───────────────▲─────────────┘
        invoke("convert_files"|             │  emit "job:update"
        "save_markdown"|"list_supported")    │  {id,path,status,markdown?,…}
                            ▼               │
            ┌────────────────────────────────────────────┐
            │  src-tauri  (markitdown-desktop_lib)         │
            │   commands + bounded background threads      │
            │   (tauri::async_runtime::spawn_blocking)     │
            └───────────────┬──────────────────────────────┘
                            │  MarkItDown::with_options(Engine::Auto)
                            ▼
            ┌────────────────────────────────────────────┐
            │  markitdown-core  (path dep, in-process)     │
            │   .convert_path() → ConvertResult            │
            └────────────────────────────────────────────┘
```

### How the queue / events work

1. The frontend assigns each dropped/picked file a job id and calls
   `convert_files({ requests: [{ id, path }] })`.
2. The Rust command emits a `queued` event per job, then spawns one
   `spawn_blocking` task per file. A small counting semaphore caps how many run
   at once (`available_parallelism`, clamped to 1–8) so a flood of files can't
   exhaust threads. The command returns immediately.
3. Each task emits `converting`, runs `MarkItDown::convert_path`, then emits
   `done` (with `markdown` + `title`) or `failed` (with `error`).
4. `main.ts` listens on `job:update` and patches its in-memory job map +
   re-renders the queue / preview live.

`save_markdown` writes the file from Rust; the path is chosen via the dialog
plugin's `save()` dialog on the JS side.

## Bundle size

Vite production output (gzip in parens):

| asset      | size      |
|------------|-----------|
| index.html | ~2.6 KB (0.9 KB) |
| CSS        | ~6.0 KB (1.9 KB) |
| JS         | ~29 KB (8.5 KB)  |
| **total**  | **~38 KB** |

Lucide is **not** shipped as a dependency: only the ~11 SVGs the UI uses are
inlined into `src/icons.ts` at author time, and no markdown library is bundled
(the renderer in `src/markdown.ts` is hand-rolled).
```
