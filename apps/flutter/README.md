# MarkItDown — Flutter Edition

A tiny, gentle, **offline** app that turns your files into clean Markdown — on
**Windows, Android, and the Web**, from a single Flutter codebase. Nothing is
uploaded; every conversion runs on your own device.

> This is an independent **Dart/Flutter reimplementation** of the excellent
> [microsoft/markitdown](https://github.com/microsoft/markitdown) Python tool,
> rebuilt as a cross-platform GUI so anyone can use it without touching a
> terminal or installing Python. All conversion logic was rewritten in pure
> Dart so it works offline on desktop, mobile, and in the browser.

## ✨ Features

- **One tap / drag-and-drop** → Markdown. No accounts, no cloud, no cost.
- **Preview & raw Markdown** side-by-side, with one-click **Copy** and **Save .md**.
- **Light & dark**, responsive layout (two-pane on desktop, single-pane on phones).
- **100% offline** — your documents never leave the device.

## 📄 Supported formats

| Category | Formats |
| --- | --- |
| Documents | PDF, DOCX (Word), EPUB |
| Spreadsheets | XLSX (Excel), CSV, TSV |
| Presentations | PPTX (PowerPoint) |
| Web & data | HTML, XML, JSON |
| Images | JPG, PNG, GIF, BMP, TIFF, WebP (EXIF metadata) |
| Text & code | TXT, Markdown, and 20+ source-code languages |
| Archives | ZIP (converts each entry inside) |

## 🚀 Run it

**Web (locally):**
```bash
flutter build web
dart run tool/serve_web.dart      # opens on localhost, auto-picks a free port
```

**Windows / Android / any device:**
```bash
flutter run -d windows            # native desktop app
flutter run -d <android-device>   # phone or emulator
```

**Build release artifacts:**
```bash
flutter build windows             # -> build/windows/x64/runner/Release/
flutter build apk                 # -> build/app/outputs/flutter-apk/app-release.apk
flutter build web                 # -> build/web/
```

## 🧱 How it works

Each format has a small, focused converter under `lib/src/converters/`:

- **DOCX / XLSX / PPTX** are parsed directly from their OpenXML (a ZIP of XML
  parts) — headings resolved through `styles.xml`, tables, links, bold/italic.
- **PDF** uses a dependency-free extractor that inflates FlateDecode content
  streams and walks the PDF text operators.
- **HTML / EPUB** go through `html2md`; **CSV/JSON/XML** render to tables/outlines.

The whole engine (`lib/src/core/` + `lib/src/converters/`) is Flutter-free pure
Dart, so it can even run from the command line:
```bash
dart run tool/convert_file.dart path/to/file.docx
```

## 🙏 Credits

- Conversion concept, format coverage, and behavior modeled on
  [microsoft/markitdown](https://github.com/microsoft/markitdown) (MIT).
- Built with [Flutter](https://flutter.dev).

## 📜 License

MIT — free for everyone, forever. See [LICENSE](LICENSE).
