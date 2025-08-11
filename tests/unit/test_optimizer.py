import unittest
from src.optimization.core.optimizer import OptimizationLoop

class TestOptimizationLoop(unittest.TestCase):
    def setUp(self):
        config = {
            "models": {
                "model1": {
                    "name": "mistral:7b",
                    "parameters": {"temperature": 0.7}
                },
                "model2": {
                    "name": "llama3.2:3b",
                    "parameters": {"temperature": 0.3}
                }
            }
        }
        self.optimizer = OptimizationLoop(config)
        
    def test_basic_optimization(self):
        result = self.optimizer.optimize_prompt(
            "Tell me about AI",
            max_iterations=2
        )
        self.assertIsNotNone(result)
        self.assertGreater(len(result.optimized_prompt), 
                          len(result.original_prompt))
        
    def test_optimization_improvement(self):
        result = self.optimizer.optimize_prompt(
            "Write a story",
            max_iterations=3
        )
        self.assertIsNotNone(result)
        self.assertGreaterEqual(result.improvement_score, 0.0)

if __name__ == '__main__':
    unittest.main()
