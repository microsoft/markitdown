from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional
from datetime import datetime


@dataclass
class ConversionRecord:
    id: Optional[int] = None
    source_path: str = ""
    output_path: Optional[str] = None
    created_at: str = field(default_factory=lambda: datetime.utcnow().isoformat())
    status: str = "queued"
    markdown_length: int = 0
    elapsed_seconds: float = 0.0
    error: Optional[str] = None

    @property
    def filename(self) -> str:
        return Path(self.source_path).name if self.source_path else ""
