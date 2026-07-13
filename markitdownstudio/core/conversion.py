import time
from pathlib import Path
from typing import Dict, List

from markitdown import MarkItDown

from .database import StudioDatabase
from .models import ConversionRecord


class ConversionService:
    def __init__(self, database: StudioDatabase):
        self.database = database
        self.converter = MarkItDown()

    def convert_file(self, source_path: str, output_dir: str) -> Dict[str, str]:
        source = Path(source_path).expanduser().resolve()
        if not source.exists():
            raise FileNotFoundError(f"File not found: {source}")

        output_dir_path = Path(output_dir).expanduser().resolve()
        output_dir_path.mkdir(parents=True, exist_ok=True)

        record = ConversionRecord(source_path=str(source), output_path="", status="queued")
        record.id = self.database.add_conversion(record)

        start = time.time()
        try:
            output_path = output_dir_path / f"{source.stem}.md"
            result = self.converter.convert(str(source))
            output_path.write_text(result.text_content or "", encoding="utf-8")
            elapsed = time.time() - start
            record.output_path = str(output_path)
            record.status = "completed"
            record.markdown_length = len(result.text_content or "")
            record.elapsed_seconds = elapsed
            self.database.update_conversion(record)
            return {"output_path": str(output_path), "markdown": result.text_content or ""}
        except Exception as exc:
            elapsed = time.time() - start
            record.status = "error"
            record.error = str(exc)
            record.elapsed_seconds = elapsed
            self.database.update_conversion(record)
            raise
