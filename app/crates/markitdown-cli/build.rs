//! Generates the man page (markitdown.1) at build time with clap_mangen.
//! The result is embedded into the binary and exposed via `--emit-man`,
//! so the shipped artifact stays a single self-contained file.

include!("src/cli.rs");

fn main() {
    println!("cargo:rerun-if-changed=src/cli.rs");
    let out_dir = std::path::PathBuf::from(std::env::var_os("OUT_DIR").expect("OUT_DIR"));

    let cmd = <Cli as clap::CommandFactory>::command()
        .version(env!("CARGO_PKG_VERSION"))
        .author("MarkItDown contributors")
        .display_name("markitdown");

    let man = clap_mangen::Man::new(cmd);
    let mut buf: Vec<u8> = Vec::new();
    man.render(&mut buf).expect("render man page");
    std::fs::write(out_dir.join("markitdown.1"), buf).expect("write man page");
}
