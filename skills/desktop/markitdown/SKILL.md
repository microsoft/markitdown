---
name: markitdown
description: Convert PDF, PPT/PPTX, DOCX, XLSX, HTML, CSV files to Markdown using Microsoft MarkItDown in the code sandbox. Use when the user says "markit", "markitdown", "down", or asks to convert/read a pdf, ppt, pptx, docx, xlsx file as markdown.
---

# markitdown

Convert uploaded files to Markdown with a script, without reading the file contents into the conversation.

## Steps
1. Run: `bash /mnt/skills/user/markitdown/scripts/md.sh "<uploaded file path>"`
   (If that path doesn't exist, locate this skill's scripts/md.sh and use it.)
2. The script prints only the output `.md` path and its size. Do NOT print the whole file.
3. Save the result to the outputs folder so the user can download it, and tell the user the filename.
4. Only show or read parts of the markdown if the user asks for a specific section or summary; use grep or head/tail for that.
5. If the output is nearly empty, the file is probably scanned images; say so.
