from __future__ import annotations

"""Utilities and data structures for bounding box sidecar emission."""

from dataclasses import dataclass, asdict, field
from typing import List, Optional, Dict, Any
import json


@dataclass
class BBoxPage:
    page: int
    width: float
    height: float


@dataclass
class BBoxLine:
    page: int
    text: str
    bbox_norm: List[float]
    bbox_abs: List[float]
    confidence: Optional[float]
    md_span: Optional[Dict[str, Optional[int]]]


@dataclass
class BBoxWord:
    page: int
    text: str
    bbox_norm: List[float]
    bbox_abs: List[float]
    confidence: Optional[float]
    line_id: int


@dataclass
class BBoxDoc:
    """Container for bounding box information."""

    version: str = "1.0"
    source: str = ""
    pages: List[BBoxPage] = field(default_factory=list)
    lines: List[BBoxLine] = field(default_factory=list)
    words: List[BBoxWord] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    def to_json(self) -> str:
        return json.dumps(self.to_dict(), ensure_ascii=False, indent=2)
