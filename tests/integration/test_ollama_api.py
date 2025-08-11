import os
import unittest
from src.models.ollama_api import OllamaAPI

class TestOllamaAPI(unittest.TestCase):
    def setUp(self):
        self.api = OllamaAPI()
        
    def test_connection(self):
        """Test API connectivity"""
        self.assertTrue(self.api.test_connection())
        
    def test_model1_generation(self):
        """Test Model1 response generation"""
        response = self.api.generate_response(
            "mistral:7b",
            "What is machine learning?",
            {"temperature": 0.7}
        )
        self.assertIsNotNone(response)
        self.assertIn("response", response)
        self.assertTrue(len(response["response"]) > 0)
        
    def test_model2_generation(self):
        """Test Model2 response generation"""
        response = self.api.generate_response(
            "llama3.2:3b",
            "Optimize this prompt: 'Write a story'",
            {"temperature": 0.3}
        )
        self.assertIsNotNone(response)
        self.assertIn("response", response)
        self.assertTrue(len(response["response"]) > 0)

if __name__ == '__main__':
    unittest.main()
