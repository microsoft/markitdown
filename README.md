# MarkItDown Desktop GUI

A production-ready, modern Windows desktop application for **Microsoft MarkItDown**, built with **Python**, **PyQt6**, and the **Fluent Design** system (via `qfluentwidgets`). 

This tool allows you to convert complex documents (PDF, Word, Excel, PowerPoint, etc.) into clean, high-fidelity Markdown files with advanced handling for tables and images.

![App Preview](gui/logo.png)

## 🚀 Key Features

- **Fluent Design UI:** A sleek, Windows 11-style dark mode interface.
- **Smart Table Recovery:** Custom-tuned logic to preserve complex multi-column tables as readable text blocks instead of broken layouts.
- **Hybrid Image Management:** 
  - Small images (<50KB) are embedded as **Base64** within the Markdown file.
  - Large images are automatically extracted to a dedicated `[filename]_assets` folder.
- **Automatic Language Detection:** Detects your Windows system language and adapts the UI (Supports English, Turkish, Spanish, French, German, and Chinese).
- **Audio Transcription:** Convert MP3/WAV files to text using built-in speech recognition (requires FFmpeg).
- **Asynchronous Processing:** Non-blocking file conversions with real-time UI logging and progress tracking.

## 🛠️ Supported Formats

- **Documents:** PDF, DOCX, XLSX, PPTX
- **Data:** CSV, JSON, XML
- **Web:** HTML, RSS, Wikipedia, YouTube (transcripts)
- **Multimedia:** MP3, WAV (Audio), JPG, PNG (OCR)
- **Archives:** ZIP, EPUB

## 📦 Installation

### Prerequisites
- **Python 3.10+**
- **FFmpeg** (Required for audio files):
  ```powershell
  winget install ffmpeg
  ```

### Local Setup
1. Clone the repository:
   ```bash
   git clone https://github.com/omererman/markitdown-desktop.git
   cd markitdown-desktop
   ```
2. Create a virtual environment:
   ```bash
   python -m venv venv
   .\venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   pip install -e "./packages/markitdown[all]"
   ```
4. Run the app:
   ```bash
   .\run_gui.bat
   ```

## 🔨 Build Standalone EXE

To generate a standalone executable for Windows:
```bash
.\build_exe.bat
```
The resulting file will be in the `dist/` directory.

## 🤝 Credits

Developed by **[OMER ERMAN](https://github.com/omererman)**.  
Powered by **Microsoft MarkItDown** and **PyQt6-Fluent-Widgets**.

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.
