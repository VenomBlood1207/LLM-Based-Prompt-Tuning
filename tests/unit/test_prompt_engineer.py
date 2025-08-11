import unittest
from src.optimization.prompt_engineer import PromptEngineer

class TestPromptEngineer(unittest.TestCase):
    def setUp(self):
        self.engineer = PromptEngineer()
        
    def test_task_detection(self):
        """Test task type detection"""
        test_cases = [
            ("What is machine learning", "general"),
            ("Write a story about space", "creative"),
            ("Compare neural networks", "analytical"),
            ("Implement a sorting algorithm", "technical")
        ]
        
        for prompt, expected_type in test_cases:
            with self.subTest(prompt=prompt):
                self.assertEqual(
                    self.engineer.detect_task_type(prompt),
                    expected_type
                )
        
    def test_prompt_enhancement(self):
        """Test prompt enhancement"""
        test_cases = [
            ("Tell me about AI", "general"),
            ("Write a story about dragons", "creative"),
            ("Analyze quantum computing", "analytical")
        ]
        
        for prompt, task_type in test_cases:
            with self.subTest(prompt=prompt):
                enhanced = self.engineer.enhance_prompt(
                    original_prompt=prompt,
                    task_type=task_type,
                    model_response="Sample response"
                )
                self.assertIn(prompt, enhanced)
                self.assertGreater(len(enhanced), len(prompt))
                
    def test_template_loading(self):
        """Test template loading"""
        self.assertIsNotNone(self.engineer.templates)
        self.assertIn("task_types", self.engineer.templates)

if __name__ == '__main__':
    unittest.main()
