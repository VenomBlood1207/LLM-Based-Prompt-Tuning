import unittest
import shutil
from pathlib import Path
from datetime import datetime
from src.data_storage.storage_manager import StorageManager
from src.data_structures.schemas import OptimizationResult

class TestStorageManager(unittest.TestCase):
    def setUp(self):
        """Set up test environment"""
        self.test_data_dir = Path("test_data")
        self.storage = StorageManager(str(self.test_data_dir))
        
    def tearDown(self):
        """Clean up test data"""
        if self.test_data_dir.exists():
            shutil.rmtree(self.test_data_dir)
            
    def test_directory_creation(self):
        """Test if directories are created properly"""
        self.assertTrue(self.test_data_dir.exists())
        self.assertTrue((self.test_data_dir / "prompts").exists())
        self.assertTrue((self.test_data_dir / "responses").exists())
        
    def test_save_and_load_result(self):
        """Test saving and loading optimization results"""
        # Create test result
        test_result = OptimizationResult(
            original_prompt="Tell me about AI",
            optimized_prompt="Explain the key concepts, applications, and impact of artificial intelligence",
            initial_response="AI is a technology...",
            final_response="Artificial Intelligence (AI) is a transformative technology...",
            improvement_score=1.5,
            created_at=datetime.now(),
            metadata={"task_type": "technical"}
        )
        
        # Save result
        self.storage.save_optimization_result(test_result)
        
        # Load recent results
        loaded_results = self.storage.load_recent_results(limit=1)
        
        # Verify
        self.assertEqual(len(loaded_results), 1)
        loaded = loaded_results[0]
        self.assertEqual(loaded.original_prompt, test_result.original_prompt)
        self.assertEqual(loaded.optimized_prompt, test_result.optimized_prompt)
        self.assertEqual(loaded.improvement_score, test_result.improvement_score)
        
    def test_multiple_results(self):
        """Test handling multiple optimization results"""
        # Create multiple test results
        results = []
        for i in range(5):
            result = OptimizationResult(
                original_prompt=f"Test prompt {i}",
                optimized_prompt=f"Optimized prompt {i}",
                initial_response=f"Initial response {i}",
                final_response=f"Final response {i}",
                improvement_score=1.0 + i,
                created_at=datetime.now(),
                metadata={"test_id": i}
            )
            results.append(result)
            self.storage.save_optimization_result(result)
            
        # Test loading with limit
        loaded = self.storage.load_recent_results(limit=3)
        self.assertEqual(len(loaded), 3)
        self.assertEqual(loaded[0].improvement_score, 5.0)
        
    def test_invalid_data(self):
        """Test handling of invalid data"""
        # Test with missing metadata
        result = OptimizationResult(
            original_prompt="Test",
            optimized_prompt="Test optimized",
            initial_response="Initial",
            final_response="Final",
            improvement_score=1.0,
            created_at=datetime.now()
        )
        
        # Should not raise exception
        self.storage.save_optimization_result(result)
        loaded = self.storage.load_recent_results(limit=1)
        self.assertEqual(len(loaded), 1)

if __name__ == '__main__':
    unittest.main()
