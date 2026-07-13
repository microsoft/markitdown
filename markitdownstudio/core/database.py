import sqlite3
from pathlib import Path
from typing import Dict, List, Optional

from .models import ConversionRecord


class StudioDatabase:
    def __init__(self, db_path: Optional[str] = None):
        self.db_path = Path(db_path or Path(__file__).resolve().parent.parent / "markitdown_studio.db")
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._init_db()

    def _init_db(self):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS conversions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    source_path TEXT NOT NULL,
                    output_path TEXT,
                    created_at TEXT NOT NULL,
                    status TEXT NOT NULL,
                    markdown_length INTEGER NOT NULL DEFAULT 0,
                    elapsed_seconds REAL NOT NULL DEFAULT 0.0,
                    error TEXT
                )
                """
            )
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS settings (
                    key TEXT PRIMARY KEY,
                    value TEXT NOT NULL
                )
                """
            )
            conn.commit()

    def add_conversion(self, record: ConversionRecord) -> int:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute(
                """
                INSERT INTO conversions (source_path, output_path, created_at, status, markdown_length, elapsed_seconds, error)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    record.source_path,
                    record.output_path,
                    record.created_at,
                    record.status,
                    record.markdown_length,
                    record.elapsed_seconds,
                    record.error,
                ),
            )
            conn.commit()
            return int(cursor.lastrowid)

    def update_conversion(self, record: ConversionRecord) -> None:
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                """
                UPDATE conversions
                SET output_path = ?, status = ?, markdown_length = ?, elapsed_seconds = ?, error = ?
                WHERE id = ?
                """,
                (
                    record.output_path,
                    record.status,
                    record.markdown_length,
                    record.elapsed_seconds,
                    record.error,
                    record.id,
                ),
            )
            conn.commit()

    def get_recent_history(self, limit: int = 20) -> List[ConversionRecord]:
        with sqlite3.connect(self.db_path) as conn:
            rows = conn.execute(
                "SELECT id, source_path, output_path, created_at, status, markdown_length, elapsed_seconds, error FROM conversions ORDER BY id DESC LIMIT ?",
                (limit,),
            ).fetchall()
        return [
            ConversionRecord(
                id=row[0],
                source_path=row[1],
                output_path=row[2],
                created_at=row[3],
                status=row[4],
                markdown_length=row[5],
                elapsed_seconds=row[6],
                error=row[7],
            )
            for row in rows
        ]

    def get_statistics(self) -> Dict[str, float]:
        with sqlite3.connect(self.db_path) as conn:
            total = conn.execute("SELECT COUNT(*) FROM conversions").fetchone()[0]
            errors = conn.execute("SELECT COUNT(*) FROM conversions WHERE status = 'error'").fetchone()[0]
            queue = conn.execute("SELECT COUNT(*) FROM conversions WHERE status = 'queued'").fetchone()[0]
            avg_seconds = conn.execute("SELECT AVG(elapsed_seconds) FROM conversions").fetchone()[0] or 0.0
        return {"total": total, "errors": errors, "queue": queue, "avg_seconds": float(avg_seconds)}

    def set_setting(self, key: str, value: str) -> None:
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("INSERT OR REPLACE INTO settings (key, value) VALUES (?, ?)", (key, value))
            conn.commit()

    def get_setting(self, key: str) -> Optional[str]:
        with sqlite3.connect(self.db_path) as conn:
            row = conn.execute("SELECT value FROM settings WHERE key = ?", (key,)).fetchone()
        return row[0] if row else None
