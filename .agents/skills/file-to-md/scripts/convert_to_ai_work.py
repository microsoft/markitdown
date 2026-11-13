"""Chuyen file nguoi dung cung cap sang Markdown va luu vao .ai-work/conversions.

Cach chay (tu thu muc goc repo):
    .venv\\Scripts\\python.exe -I .agents\\skills\\file-to-md\\scripts\\convert_to_ai_work.py \
        --name <short-name> <file-hoac-thu-muc> [<file-hoac-thu-muc> ...]

Ket qua:
    .ai-work/conversions/<yyyy-mm-dd>-<short-name>/
        00-manifest.md        bang tong hop nguon -> dich, trang thai, loi
        <ten-file-goc>.md     noi dung Markdown cua tung file

Ma thoat: 0 = tat ca thanh cong, 1 = co file loi hoac bi bo qua, 2 = loi tham so.
"""

from __future__ import annotations

import argparse
import datetime as dt
import glob
import hashlib
import os
import re
import shutil
import sys
import unicodedata
from pathlib import Path

# Dinh dang can goi dich vu truc tuyen (gui du lieu ra khoi may).
ONLINE_EXTENSIONS = {".mp3", ".wav", ".m4a", ".mp4", ".aac", ".flac", ".ogg", ".wma"}

# Bo qua cac file he thong / tam.
SKIP_NAMES = {"thumbs.db", "desktop.ini", ".ds_store"}

REPO_ROOT = Path(__file__).resolve().parents[4]
CONVERSIONS_DIR = REPO_ROOT / ".ai-work" / "conversions"


def ensure_ffmpeg_on_path() -> str | None:
    """Them ffmpeg vao PATH cua tien trinh neu chua co (winget/chocolatey)."""
    found = shutil.which("ffmpeg")
    if found:
        return found
    candidates: list[str] = []
    local = os.environ.get("LOCALAPPDATA")
    if local:
        candidates += glob.glob(
            os.path.join(local, "Microsoft", "WinGet", "Packages", "Gyan.FFmpeg*", "*", "bin")
        )
        candidates.append(os.path.join(local, "Microsoft", "WinGet", "Links"))
    candidates.append(r"C:\ProgramData\chocolatey\bin")
    for folder in candidates:
        if os.path.isfile(os.path.join(folder, "ffmpeg.exe")):
            os.environ["PATH"] = folder + os.pathsep + os.environ.get("PATH", "")
            return os.path.join(folder, "ffmpeg.exe")
    return None


def slugify(text: str) -> str:
    text = text.strip().lower().replace("đ", "d")
    text = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode("ascii")
    text = re.sub(r"[^a-z0-9\-]+", "-", text)
    return re.sub(r"-{2,}", "-", text).strip("-") or "files"


def collect_inputs(paths: list[str]) -> tuple[list[tuple[Path, Path]], list[str]]:
    """Tra ve danh sach (file, ten-tuong-doi-de-dat-ten-output) va danh sach duong dan khong ton tai."""
    files: list[tuple[Path, Path]] = []
    missing: list[str] = []
    for raw in paths:
        p = Path(raw).expanduser()
        if p.is_file():
            files.append((p.resolve(), Path(p.name)))
        elif p.is_dir():
            base = p.resolve()
            for f in sorted(base.rglob("*")):
                if f.is_file() and f.name.lower() not in SKIP_NAMES and not f.name.startswith("~$"):
                    files.append((f, Path(base.name) / f.relative_to(base)))
        else:
            missing.append(raw)
    return files, missing


def unique_path(path: Path, taken: set[Path]) -> Path:
    candidate = path
    i = 2
    while candidate.exists() or candidate in taken:
        candidate = path.with_name(f"{path.stem}-{i}{path.suffix}")
        i += 1
    taken.add(candidate)
    return candidate


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def human_size(n: int) -> str:
    for unit in ("B", "KB", "MB", "GB"):
        if n < 1024 or unit == "GB":
            return f"{n:.0f} {unit}" if unit == "B" else f"{n:.1f} {unit}"
        n /= 1024
    return f"{n} B"


def md_cell(text: str) -> str:
    return str(text).replace("|", "\\|").replace("\n", " ")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("inputs", nargs="+", help="File hoac thu muc can chuyen")
    parser.add_argument("--name", required=True, help="Ten ngan cho dot chuyen doi, vd: hop-dong-abc")
    parser.add_argument("--date", default=dt.date.today().isoformat(), help="Ngay (yyyy-mm-dd), mac dinh hom nay")
    parser.add_argument(
        "--allow-online",
        action="store_true",
        help="Cho phep chuyen audio (gui am thanh len dich vu nhan dang giong noi truc tuyen)",
    )
    args = parser.parse_args()

    try:
        from markitdown import MarkItDown
    except ImportError:
        print("LOI: chua cai markitdown trong moi truong Python nay. Xem .agents/rules/build.md.", file=sys.stderr)
        return 2

    files, missing = collect_inputs(args.inputs)
    if not files and not missing:
        print("LOI: khong tim thay file nao de chuyen.", file=sys.stderr)
        return 2

    out_dir = CONVERSIONS_DIR / f"{args.date}-{slugify(args.name)}"
    out_dir.mkdir(parents=True, exist_ok=True)

    ffmpeg = ensure_ffmpeg_on_path()
    md = MarkItDown()
    taken: set[Path] = set()
    rows: list[dict[str, str]] = []

    for raw in missing:
        rows.append({"src": raw, "dst": "", "size": "", "sha": "", "status": "MISSING", "note": "Duong dan khong ton tai"})

    for src, rel in files:
        size = src.stat().st_size
        row = {"src": str(src), "dst": "", "size": human_size(size), "sha": sha256(src)[:12], "status": "", "note": ""}
        ext = src.suffix.lower()
        if ext in ONLINE_EXTENSIONS and not args.allow_online:
            row.update(status="SKIPPED", note="Audio can gui du lieu len dich vu truc tuyen; chay lai voi --allow-online neu nguoi dung dong y")
            rows.append(row)
            continue
        if ext in ONLINE_EXTENSIONS and not ffmpeg:
            row.update(status="FAILED", note="Khong tim thay ffmpeg")
            rows.append(row)
            continue
        target = unique_path(out_dir / rel.parent / f"{rel.name}.md", taken)
        try:
            result = md.convert(str(src))
            text = result.text_content or ""
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(text, encoding="utf-8")
            row["dst"] = target.relative_to(out_dir).as_posix()
            if text.strip():
                row["status"] = "OK"
                row["note"] = f"{len(text):,} ky tu"
            else:
                row["status"] = "EMPTY"
                row["note"] = "Khong trich duoc chu (co the la PDF scan/anh) - can OCR"
        except Exception as exc:  # noqa: BLE001 - ghi nhan moi loi vao manifest
            row.update(status="FAILED", note=f"{type(exc).__name__}: {exc}".splitlines()[0][:300])
        rows.append(row)

    counts: dict[str, int] = {}
    for r in rows:
        counts[r["status"]] = counts.get(r["status"], 0) + 1

    lines = [
        f"# Conversion manifest — {args.date}-{slugify(args.name)}",
        "",
        f"- Thoi diem: {dt.datetime.now().strftime('%Y-%m-%d %H:%M')}",
        f"- Thu muc ket qua: `{out_dir.relative_to(REPO_ROOT).as_posix()}`",
        f"- Tong so: {len(rows)} — " + ", ".join(f"{k}: {v}" for k, v in sorted(counts.items())),
        "",
        "| # | Nguon | Ket qua | Kich thuoc | SHA-256 (12) | Trang thai | Ghi chu |",
        "|---|---|---|---|---|---|---|",
    ]
    for i, r in enumerate(rows, 1):
        dst = f"[{md_cell(r['dst'])}]({r['dst'].replace(' ', '%20')})" if r["dst"] else ""
        lines.append(
            f"| {i} | {md_cell(r['src'])} | {dst} | {r['size']} | {r['sha']} | {r['status']} | {md_cell(r['note'])} |"
        )
    manifest = out_dir / "00-manifest.md"
    if manifest.exists():
        old = manifest.read_text(encoding="utf-8")
        lines = [old.rstrip(), "", "---", ""] + lines
    manifest.write_text("\n".join(lines) + "\n", encoding="utf-8")

    sys.stdout.reconfigure(encoding="utf-8")
    print(f"OUTPUT_DIR={out_dir}")
    print(f"MANIFEST={manifest}")
    for r in rows:
        print(f"{r['status']:8} {r['src']} -> {r['dst']} {r['note']}")
    return 0 if all(r["status"] == "OK" for r in rows) else 1


if __name__ == "__main__":
    sys.exit(main())
