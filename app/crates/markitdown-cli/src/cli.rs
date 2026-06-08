// Command-line definition. This file is `include!`d by build.rs to generate
// the man page, so it must only depend on `clap` (not on markitdown-core).

use clap::Parser;

#[derive(Debug, Clone, Copy, PartialEq, Eq, clap::ValueEnum)]
pub enum EngineArg {
    /// Pure-Rust converters (default; zero external dependencies).
    Rust,
    /// The optional PyInstaller-compiled Python markitdown binary.
    Python,
    /// Rust first, Python fallback when configured and needed (e.g. OCR).
    Auto,
}

#[derive(Parser, Debug)]
#[command(
    name = "markitdown",
    about = "Convert files and URIs (PDF, Office, HTML, images, audio, …) to Markdown",
    long_about = "A self-contained, dependency-free Rust port of Microsoft MarkItDown.\n\
                  Converts PDF, DOCX, XLSX/XLS, PPTX, HTML, CSV, EPUB, ZIP, Jupyter \
                  notebooks, Outlook .msg, RSS/Atom feeds, images (EXIF), audio \
                  (tags) and plain text/JSON into Markdown for humans and LLMs.\n\n\
                  Reads from FILES (paths or file:/data:/http(s): URIs) or stdin.",
    after_help = "EXAMPLES:\n  \
        markitdown report.pdf                     # to stdout\n  \
        markitdown report.pdf -o report.md        # to file\n  \
        cat report.pdf | markitdown -x pdf        # stdin with extension hint\n  \
        markitdown a.pdf b.docx c.xlsx -O out/    # parallel batch\n  \
        markitdown https://example.com/page.html  # fetch + convert\n  \
        markitdown --emit-man | mandoc | less     # view the manual (macOS)\n  \
        markitdown --emit-man | man -l -          # view the manual (Linux)",
    disable_version_flag = true
)]
pub struct Cli {
    /// Files or URIs to convert; reads stdin when omitted.
    pub inputs: Vec<String>,

    /// Output file (single input only; default: stdout).
    #[arg(short, long, value_name = "FILE")]
    pub output: Option<std::path::PathBuf>,

    /// Output directory for batch conversion; each input becomes <stem>.md.
    #[arg(short = 'O', long, value_name = "DIR", conflicts_with = "output")]
    pub output_dir: Option<std::path::PathBuf>,

    /// Extension hint for stdin/extension-less input (e.g. pdf or .pdf).
    #[arg(short = 'x', long, value_name = "EXT")]
    pub extension: Option<String>,

    /// MIME type hint (e.g. application/pdf).
    #[arg(short = 'm', long, value_name = "TYPE")]
    pub mime_type: Option<String>,

    /// Charset hint for text input (e.g. UTF-8, shift_jis).
    #[arg(short = 'c', long, value_name = "CHARSET")]
    pub charset: Option<String>,

    /// Keep base64 data: URIs in the output instead of truncating them.
    #[arg(long)]
    pub keep_data_uris: bool,

    /// Conversion engine. `auto` = pure Rust, transparently retrying with the
    /// optional Python engine (MARKITDOWN_PY_BIN) when Rust hits a fidelity
    /// gap (scanned PDF, DOCX comments/equations, RTF email body, OCR,
    /// transcription). Costs nothing when no Python binary is configured.
    #[arg(long, value_enum, default_value = "auto")]
    pub engine: EngineArg,

    /// Path to the optional Python fallback binary (overrides MARKITDOWN_PY_BIN).
    #[arg(long, value_name = "PATH")]
    pub python_bin: Option<std::path::PathBuf>,

    // ---- LLM image captions (any OpenAI-compatible API, incl. local LLMs) ----
    /// Provider preset: openai | ollama | lmstudio | openrouter | groq | custom.
    /// Sets the base URL (unless --llm-api-base is given). See --list-llm-providers.
    #[arg(long, value_name = "ID")]
    pub llm_provider: Option<String>,

    /// LLM API key for image captioning (overrides MARKITDOWN_LLM_API_KEY).
    #[arg(long, value_name = "KEY")]
    pub llm_api_key: Option<String>,

    /// Vision model for captioning, e.g. gpt-4o-mini, or a local model like
    /// `llava` / `llama3.2-vision` (overrides MARKITDOWN_LLM_MODEL).
    #[arg(long, value_name = "MODEL")]
    pub llm_model: Option<String>,

    /// OpenAI-compatible base URL (overrides MARKITDOWN_LLM_API_BASE). Point at
    /// a local server for offline captions, e.g. Ollama
    /// `http://localhost:11434/v1` or LM Studio `http://localhost:1234/v1`.
    #[arg(long, value_name = "URL")]
    pub llm_api_base: Option<String>,

    /// Custom caption prompt (overrides MARKITDOWN_LLM_PROMPT).
    #[arg(long, value_name = "TEXT")]
    pub llm_prompt: Option<String>,

    /// Report which engines/capabilities are available (Python fallback, LLM
    /// captions, model, endpoint) and exit. No secrets are printed.
    #[arg(long)]
    pub check: bool,

    /// List the built-in LLM provider presets (id, base URL, example models)
    /// and exit.
    #[arg(long)]
    pub list_llm_providers: bool,

    /// List supported formats and exit.
    #[arg(long)]
    pub list_formats: bool,

    /// Print the roff man page to stdout and exit (pipe to mandoc/man, or
    /// install: markitdown --emit-man > /usr/local/share/man/man1/markitdown.1).
    #[arg(long)]
    pub emit_man: bool,

    /// Print version and exit.
    #[arg(short = 'v', long)]
    pub version: bool,
}
