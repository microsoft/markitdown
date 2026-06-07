# markitdown (CLI)

Single self-contained binary (~6 MB, no runtime dependencies) converting
documents to Markdown. Flags mirror the Python `markitdown` CLI, plus parallel
batch mode.

```bash
cargo build --release -p markitdown-cli   # → ../target/release/markitdown
```

## Usage

```bash
markitdown report.pdf                      # stdout
markitdown report.pdf -o report.md        # file
cat report.pdf | markitdown -x pdf        # stdin with extension hint
markitdown doc.bin -m application/pdf     # mimetype hint
markitdown data.csv -c shift_jis          # charset hint
markitdown a.pdf b.docx c.html -O out/    # batch: all cores via rayon
markitdown https://en.wikipedia.org/wiki/Rust  # URLs convert directly
markitdown --list-formats
markitdown big-scan.pdf                   # auto (default): Python fallback for
                                          # OCR & co. when MARKITDOWN_PY_BIN is set
markitdown --engine rust file.docx        # pin pure Rust
markitdown --engine python file.pdf       # force full Python fidelity
```

Name collisions in batch mode keep the original extension
(`test.docx` + `test.xlsx` → `test.docx.md`, `test.xlsx.md`).

## Man page

Generated at build time by `clap_mangen` and embedded in the binary:

```bash
markitdown --emit-man | mandoc | less                                  # view (macOS)
markitdown --emit-man | man -l -                                       # view (Linux)
markitdown --emit-man | sudo tee /usr/local/share/man/man1/markitdown.1 >/dev/null
man markitdown                                                          # after install
```

## Exit codes

`0` success · `1` any conversion/IO failure (batch: nonzero if *any* input
failed; per-file status lines go to stderr).

## Tests

`cargo test -p markitdown-cli` — unit tests plus integration tests that run
the real binary against the Python suite's fixtures (stdout, stdin hints,
`-o`, batch, man page, error paths).
