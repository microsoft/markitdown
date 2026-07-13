\# MarkItDown Studio



\## Objective



Create a production-quality Windows desktop application for converting documents into Markdown using Microsoft's MarkItDown library.



The application is intended for personal use as part of the AI Factory ecosystem.



The UI should resemble a modern Microsoft Office / Visual Studio style desktop application.



\---



\# Technology



Python 3.12



PySide6



Microsoft MarkItDown



SQLite



Watchdog



PyMuPDF



Pillow



PyInstaller



\---



\# Architecture



app.py



/ui



/core



/database



/assets



/icons



/themes



/plugins



\---



\# UI



Dark theme



Rounded cards



Modern toolbar



Left navigation



Resizable panels



Dock widgets



Status bar



Progress indicators



Professional icons



\---



\# Navigation



Home



Single File



Batch Convert



Folder Watcher



History



Obsidian



AI Tools



OCR



Settings



About



\---



\# Home



Large Drag \& Drop area



Browse File



Browse Folder



Recent Files



Statistics Cards



Total Converted



Errors



Queue



Average Time



Recent Activity



\---



\# Single File



Convert one document.



Preview document.



Preview markdown.



Copy markdown.



Open output.



\---



\# Batch



Queue



Start



Pause



Resume



Cancel



Retry



Remove



Clear Queue



\---



\# Queue Columns



Filename



Type



Progress



Status



Elapsed



Output



Actions



\---



\# Folder Watcher



Monitor folders.



Automatically convert new files.



Maintain folder hierarchy.



Ignore duplicate files.



\---



\# Supported Formats



PDF



DOCX



PPTX



XLSX



HTML



EPUB



ZIP



Images



Audio



Everything supported by MarkItDown.



\---



\# Output



Markdown



Text



HTML



JSON



\---



\# Obsidian Mode



Generate YAML



Preserve folders



Wiki links



Tags



Attachments



Daily notes compatibility



\---



\# AI Page



Placeholder.



Future Ollama integration.



Future ChatGPT integration.



Future Claude integration.



Future Gemini integration.



\---



\# OCR



If image



Extract text.



If scanned PDF



OCR first.



Then convert.



\---



\# Settings



Theme



Output folder



Overwrite



Preserve folders



Workers



History



Logging



Auto Open



\---



\# Logging



Timestamp



Severity



Export



Clear



\---



\# Database



SQLite



Conversion history



Settings



Recent files



Recent folders



\---



\# Packaging



requirements.txt



README.md



build.ps1



build.bat



PyInstaller spec



Application icon placeholder



\---



\# Coding Standards



Use classes.



Separate UI from logic.



Thread-safe conversion.



Signals and slots.



Responsive UI.



No blocking operations.



Professional comments.



Type hints.



PEP8.



