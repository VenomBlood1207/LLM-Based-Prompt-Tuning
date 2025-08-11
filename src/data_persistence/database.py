import sqlite3
from pathlib import Path
from datetime import datetime

class DatabaseManager:
    def __init__(self, db_path="data/optimization.db"):
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._init_db()

    def _init_db(self):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS optimization_results (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    original_prompt TEXT,
                    optimized_prompt TEXT,
                    initial_response TEXT,
                    final_response TEXT,
                    improvement_score REAL,
                    task_type TEXT,
                    created_at TEXT,
                    metadata TEXT
                )
            """)
            conn.commit()

    def save_result(self, result):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO optimization_results (
                    original_prompt, optimized_prompt, initial_response, final_response,
                    improvement_score, task_type, created_at, metadata
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                result.original_prompt,
                result.optimized_prompt,
                result.initial_response,
                result.final_response,
                result.improvement_score,
                result.metadata.get("task_type", "") if result.metadata else "",
                result.created_at.isoformat(),
                str(result.metadata)
            ))
            conn.commit()

    def fetch_recent(self, limit=5):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT original_prompt, optimized_prompt, initial_response, final_response,
                       improvement_score, task_type, created_at, metadata
                FROM optimization_results
                ORDER BY created_at DESC
                LIMIT ?
            """, (limit,))
            return cursor.fetchall()