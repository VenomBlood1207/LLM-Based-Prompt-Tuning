import unittest
from src.evaluation.metrics1 import MetricsCalculator

class TestMetricsCalculator(unittest.TestCase):
    def setUp(self):
        self.calculator = MetricsCalculator()
        
    def test_basic_metrics(self):
        """Test basic metrics calculation"""
        original_prompt = "Tell me about AI"
        optimized_prompt = "Explain the key concepts, applications, and future implications of Artificial Intelligence"
        original_response = "AI is a technology."
        optimized_response = "Artificial Intelligence (AI) is a transformative technology that enables machines to simulate human intelligence through learning, reasoning, and problem-solving capabilities."
        
        metrics = self.calculator.calculate_metrics(
            original_prompt,
            optimized_prompt,
            original_response,
            optimized_response
        )
        
        self.assertGreater(metrics.prompt_length, 1.0)
        self.assertGreater(metrics.response_length, 1.0)
        self.assertGreater(metrics.improvement_ratio, 0.0)
        self.assertLessEqual(metrics.coherence_score, 1.0)
        self.assertLessEqual(metrics.task_completion, 1.0)
        
    def test_summary_statistics(self):
        """Test summary statistics calculation"""
        # Add multiple test cases
        test_cases = [
            ("What is Python?", "Explain Python programming language, its features, and applications",
             "Python is a language", "Python is a high-level, interpreted programming language known for its simplicity and versatility."),
            ("Write a story", "Write a creative story about a magical forest with detailed character descriptions",
             "Once upon a time", "Deep in the enchanted forest, ancient trees whispered secrets to those who dared to listen.")
        ]
        
        for orig_prompt, opt_prompt, orig_resp, opt_resp in test_cases:
            self.calculator.calculate_metrics(orig_prompt, opt_prompt, orig_resp, opt_resp)
            
        summary = self.calculator.get_summary_statistics()
        
        self.assertIn("avg_improvement", summary)
        self.assertIn("avg_coherence", summary)
        self.assertIn("avg_task_completion", summary)
        self.assertIn("overall_score", summary)

if __name__ == '__main__':
    unittest.main()
