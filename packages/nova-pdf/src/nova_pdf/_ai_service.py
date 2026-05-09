"""AI service using zai-sdk and glm-ocr."""

import base64
import re
from dataclasses import dataclass
from typing import BinaryIO, Optional

from ._config import NovaPdfConfig

try:
    from zai import ZhipuAiClient
except ImportError:
    ZhipuAiClient = None


@dataclass
class AIResult:
    """Result from AI conversion."""
    text: str
    success: bool = True
    error: Optional[str] = None


class AIService:
    """
    AI Service using zai-sdk + glm-ocr.
    
    Features:
    - Direct API call to glm-ocr layout_parsing
    - Support image bytes via base64 data URI
    - Return Markdown or HTML format content
    """
    
    def __init__(
        self,
        api_key: Optional[str] = None,
        model: str = "glm-ocr",
        timeout: int = 120,
        config: Optional[NovaPdfConfig] = None,
    ):
        if ZhipuAiClient is None:
            raise ImportError(
                "zai-sdk is required. Install with: pip install nova-pdf[zhipu]"
            )
        
        if config:
            self.api_key = api_key or config.zhipu_api_key
            self.model = model or config.model
            self.timeout = timeout or config.timeout
        else:
            config = NovaPdfConfig.load()
            self.api_key = api_key or config.zhipu_api_key
            self.model = model
            self.timeout = timeout
        
        if not self.api_key:
            raise ValueError(
                "API key is required. Set NOVA_ZHIPU_API_KEY environment variable"
            )
        
        self.client = ZhipuAiClient(api_key=self.api_key)
    
    def image_to_markdown(
        self,
        image_stream: BinaryIO,
        filename: str = "page.png",
        keep_html: bool = False,
    ) -> AIResult:
        """
        Convert image to Markdown using glm-ocr.
        
        Args:
            image_stream: Image stream
            filename: Filename (for content type detection)
            keep_html: Keep HTML format for complex tables (default: False, convert to MD)
        
        Returns:
            AIResult: Conversion result
        """
        try:
            image_stream.seek(0)
            image_bytes = image_stream.read()
            
            base64_image = base64.b64encode(image_bytes).decode("utf-8")
            content_type = "image/jpeg" if filename.lower().endswith((".jpg", ".jpeg")) else "image/png"
            data_uri = f"data:{content_type};base64,{base64_image}"
            
            response = self.client.layout_parsing.create(
                model=self.model,
                file=data_uri
            )
            
            # Get HTML content
            html = response.md_results or ""
            
            if not html and response.layout_details:
                parts = []
                for detail_list in response.layout_details:
                    for detail in detail_list:
                        if detail.content:
                            parts.append(detail.content)
                html = "\n".join(parts)
            
            # Convert to Markdown or keep HTML
            if keep_html:
                text = html.strip()
            else:
                text = self._html_to_markdown(html.strip()) if html else ""
            
            return AIResult(text=text, success=True)
        
        except Exception as e:
            return AIResult(text="", success=False, error=str(e))
        finally:
            image_stream.seek(0)
    
    def _html_to_markdown(self, html: str) -> str:
        """Convert HTML to Markdown."""
        if not html:
            return ""
        
        # Extract titles from <div>
        titles = []
        div_pattern = r'<div[^>]*>(.*?)</div>'
        for match in re.finditer(div_pattern, html, re.DOTALL | re.IGNORECASE):
            title = re.sub(r'<[^>]+>', '', match.group(1)).strip()
            if title:
                titles.append(title)
        
        # Remove <div> from HTML
        html = re.sub(div_pattern, '', html, flags=re.DOTALL | re.IGNORECASE)
        
        # Check for table
        if '<table' in html.lower():
            table_md = self._convert_html_table(html)
            if titles:
                return f"**{' '.join(titles)}**\n\n{table_md}"
            return table_md
        
        # Plain text
        text = re.sub(r'<[^>]+>', '', html).strip()
        if titles:
            return f"**{' '.join(titles)}**\n\n{text}"
        return text
    
    def _convert_html_table(self, html: str) -> str:
        """Convert HTML table to Markdown table."""
        # Parse rows
        rows = []
        rowspan_cells = {}
        
        for row_idx, row_match in enumerate(re.finditer(r'<tr[^>]*>(.*?)</tr>', html, re.DOTALL | re.IGNORECASE)):
            cells = []
            col_idx = 0
            
            # Fill rowspan cells
            while (row_idx, col_idx) in rowspan_cells:
                cells.append(rowspan_cells[(row_idx, col_idx)])
                col_idx += 1
            
            # Parse cells
            for cell_match in re.finditer(r'<td([^>]*)>(.*?)</td>', row_match.group(1), re.DOTALL | re.IGNORECASE):
                attrs, content = cell_match.groups()
                content = re.sub(r'<[^>]+>', '', content).strip().replace('\n', ' ')
                
                rowspan = int(r.group(1)) if (r := re.search(r'rowspan\s*=\s*["\']?(\d+)', attrs, re.IGNORECASE)) else 1
                colspan = int(c.group(1)) if (c := re.search(r'colspan\s*=\s*["\']?(\d+)', attrs, re.IGNORECASE)) else 1
                
                cells.append(content)
                cells.extend([""] * (colspan - 1))
                
                if rowspan > 1:
                    for r in range(1, rowspan):
                        for c in range(colspan):
                            rowspan_cells[(row_idx + r, col_idx + c)] = content
                
                col_idx += colspan
            
            # Fill remaining rowspan
            while (row_idx, col_idx) in rowspan_cells:
                cells.append(rowspan_cells[(row_idx, col_idx)])
                col_idx += 1
            
            rows.append(cells)
        
        if not rows:
            return ""
        
        # Normalize
        max_cols = max(len(row) for row in rows)
        for row in rows:
            row.extend([""] * (max_cols - len(row)))
        
        # Simple output: first row as header
        md_lines = []
        for i, row in enumerate(rows):
            md_row = "| " + " | ".join(c or " " for c in row) + " |"
            md_lines.append(md_row)
            if i == 0:
                md_lines.append("|" + "|".join(["---"] * max_cols) + "|")
        
        return "\n".join(md_lines)
