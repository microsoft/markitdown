import json
import re

def convert_markdown_to_json(md_text: str) -> dict:
    """
    Parses Markdown text and structures it into a JSON-serializable dictionary
    containing a title and sections.
    """
    lines = md_text.splitlines()
    title = "Untitled Document"
    sections = []
    
    current_heading = "Introduction"
    current_content = []

    for line in lines:
        if line.startswith("# "):
            title = line[2:].strip()
        elif re.match(r"^#{2,} ", line):
            # Save the previous section before starting a new one
            if current_content or current_heading != "Introduction":
                sections.append({
                    "heading": current_heading,
                    "content": "\n".join(current_content).strip()
                })
            current_heading = re.sub(r"^#{2,} ", "", line).strip()
            current_content = []
        else:
            current_content.append(line)

    if current_content:
        sections.append({
            "heading": current_heading,
            "content": "\n".join(current_content).strip()
        })

    return {
        "title": title,
        "sections": sections
    }