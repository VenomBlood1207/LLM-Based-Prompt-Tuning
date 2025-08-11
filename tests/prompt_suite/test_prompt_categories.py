import unittest
import sqlite3
import json
from src.optimization.core.optimizer import OptimizationLoop
from src.data_persistence.database import DatabaseManager
from src.data_structures.schemas import OptimizationResult
from src.optimization.prompt_engineer import PromptEngineer

class TestPromptCategories(unittest.TestCase):
    def setUp(self):
        self.db_path = "test_data/test_optimization.db"
        self.optimizer = OptimizationLoop({
            "models": {
                "model1": {"name": "mistral:7b", "parameters": {"temperature": 0.7}},
                "model2": {"name": "llama3.2:3b", "parameters": {"temperature": 0.3}}
            }
        })
        self.db = DatabaseManager(self.db_path)
        self.engineer = PromptEngineer()

    def test_prompt_categories(self):
        prompts = {
            "general": "What is artificial intelligence?",
            "technical": "Explain how a neural network learns.",
            "creative": "Write a poem about the ocean.",
            "analytical": "Compare solar and wind energy."
        }
        for task_type, prompt in prompts.items():
            with self.subTest(task_type=task_type):
                result = self.optimizer.optimize_prompt(prompt, max_iterations=1)
                self.assertIsInstance(result, OptimizationResult)
                self.db.save_result(result)
                print(f"Saved result for {task_type} prompt.")

        # Print database contents after saving results
        print("\nDatabase contents:")
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM optimization_results")
        columns = [description[0] for description in cursor.description]
        rows = cursor.fetchall()
        if not rows:
            print("No results found in the database.")
        for row in rows:
            record = dict(zip(columns, row))
            # Pretty print metadata if it's a dict-like string
            if record.get("metadata"):
                try:
                    record["metadata"] = json.loads(record["metadata"].replace("'", '"'))
                except Exception:
                    pass
            print(json.dumps(record, indent=2, default=str))
            print("-" * 40)
        conn.close()

    def test_role_prompt(self):
        prompt = "Explain quantum computing"
        enhanced = self.engineer.enhance_prompt(prompt, task_type="role", model_response="Sample response", role="physics professor")
        self.assertIn("physics professor", enhanced)

if __name__ == '__main__':
    unittest.main()
