import unittest
import os
from datetime import datetime
from src.data_persistence.database import DatabaseManager
from src.data_structures.schemas import OptimizationResult

class TestDatabaseManager(unittest.TestCase):
    def setUp(self):
        self.test_db_path = "test_data/test_optimization.db"
        os.makedirs("test_data", exist_ok=True)
        self.db = DatabaseManager(self.test_db_path)

    def tearDown(self):
        if os.path.exists(self.test_db_path):
            os.remove(self.test_db_path)

    def test_save_and_fetch(self):
        result = OptimizationResult(
            original_prompt="What is AI?",
            optimized_prompt="Explain artificial intelligence in detail.",
            initial_response="AI is...",
            final_response="Artificial intelligence is...",
            improvement_score=1.2,
            created_at=datetime.now(),
            metadata={"task_type": "general"}
        )
        self.db.save_result(result)
        rows = self.db.fetch_recent(limit=1)
        self.assertEqual(len(rows), 1)
        self.assertIn("What is AI?", rows[0][0])

if __name__ == '__main__':
    unittest.main()
