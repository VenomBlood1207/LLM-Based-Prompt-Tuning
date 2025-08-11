import sys
from pathlib import Path
import logging
from typing import Dict, Optional
from datetime import datetime
sys.path.append(str(Path(__file__).parent.parent.parent))

from src.models.ollama_api import OllamaAPI
from src.data_structures.schemas import PromptResponse, OptimizationResult
from src.logging.monitor import PerformanceMonitor
from src.config.config_manager import ConfigManager
from ..data_storage.storage_manager import StorageManager

class PromptOptimizationPipeline:
    def __init__(self, config: Dict):
        self.config = config
        self.storage = StorageManager()
        self.model1 = OllamaAPI()  # Task executor
        self.model2 = OllamaAPI()  # Prompt optimizer
        self.logger = logging.getLogger(__name__)
        self.monitor = PerformanceMonitor(config)
        self.prompt_engineer = PromptEngineer()
        
    def optimize_prompt(self, 
                       original_prompt: str,
                       task_type: str = "general") -> OptimizationResult:
        """
        Main optimization pipeline
        """
        start_time = datetime.now()
        try:
            # Detect task type if not provided
            if task_type is None:
                task_type = self.prompt_engineer.detect_task_type(original_prompt)
            
            # Get enhanced prompt
            enhanced_prompt = self.prompt_engineer.enhance_prompt(
                original_prompt,
                task_type
            )

            # Step 1: Get initial response from Model1
            initial_response = self.model1.generate_response(
                model=self.config["models"]["model1"]["name"],
                prompt=original_prompt,
                params=self.config["models"]["model1"]["parameters"]
            )
            
            if not initial_response:
                raise Exception("Failed to get initial response")
            
            # Step 2: Analyze and optimize prompt using Model2
            optimization_prompt = self._create_optimization_prompt(
                original_prompt, 
                initial_response["response"],
                task_type
            )
            
            optimized = self.model2.generate_response(
                model=self.config["models"]["model2"]["name"],
                prompt=optimization_prompt,
                params=self.config["models"]["model2"]["parameters"]
            )
            
            if not optimized:
                raise Exception("Failed to optimize prompt")
            
            # Step 3: Test optimized prompt
            final_response = self.model1.generate_response(
                model=self.config["models"]["model1"]["name"],
                prompt=optimized["response"],
                params=self.config["models"]["model1"]["parameters"]
            )
            
            result = OptimizationResult(
                original_prompt=original_prompt,
                optimized_prompt=optimized["response"],
                initial_response=initial_response["response"],
                final_response=final_response["response"],
                improvement_score=self._calculate_improvement(
                    initial_response["response"],
                    final_response["response"]
                ),
                created_at=datetime.now(),
                metadata={
                    "task_type": task_type,
                    "duration": (datetime.now() - start_time).total_seconds()
                }
            )
            
            # Log performance metrics
            self.monitor.log_optimization(result)
            return result
            
        except Exception as e:
            self.logger.error(f"Optimization failed: {str(e)}")
            return None
            
    def _create_optimization_prompt(self, 
                                  original: str, 
                                  response: str,
                                  task_type: str) -> str:
        """Create prompt for Model2"""
        template = self._load_template(task_type)
        return template.format(
            original_prompt=original,
            model_response=response,
            task_type=task_type
        )
        
    def _calculate_improvement(self, 
                             initial: str, 
                             final: str) -> float:
        """Calculate improvement score based on response length and quality"""
        # Basic improvement metric
        length_ratio = len(final) / len(initial) if len(initial) > 0 else 0
        
        # TODO: Add more sophisticated metrics
        # - Semantic similarity
        # - Response coherence
        # - Task-specific metrics
        
        return length_ratio
        
    def _load_template(self, task_type: str) -> str:
        """Load appropriate template for task type"""
        templates = self.config.get("templates", {})
        return templates.get(task_type, templates["base_optimization_template"])
        
    def save_performance_stats(self):
        """Save performance monitoring data"""
        self.monitor.save_stats()
        return self.monitor.get_summary()


if __name__ == "__main__":
    # Configure logging
    logging.basicConfig(level=logging.INFO)
    
    # Test configuration
    config = {
        "models": {
            "model1": {
                "name": "mistral:7b",  # Changed from mistral:7b
                "parameters": {
                    "temperature": 0.7,
                    "max_tokens": 2048
                }
            },
            "model2": {
                "name": "llama3.2:3b",   # Changed from llama2:3b
                "parameters": {
                    "temperature": 0.3,
                    "max_tokens": 512
                }
            }
        },
        "templates": {
            "base_optimization_template": """
            You are an expert prompt optimizer. Analyze this prompt and response:
            
            ORIGINAL PROMPT: {original_prompt}
            MODEL RESPONSE: {model_response}
            TASK TYPE: {task_type}
            
            Create an improved version of the original prompt that will:
            1. Be more specific and clear
            2. Include relevant context
            3. Better guide the model's response
            4. Maintain the original intent
            
            Provide ONLY the optimized prompt with no additional explanation.
            """
        }
    }
    
    # Test the pipeline
    pipeline = PromptOptimizationPipeline(config)
    
    test_prompts = [
        ("Tell me about machine learning", "general"),
        ("Write a story", "creative"),
        ("Explain quantum computing", "technical")
    ]
    
    print("\nTesting Prompt Optimization Pipeline...")
    print("=" * 50)
    
    for prompt, task_type in test_prompts:
        print(f"\nOptimizing prompt: '{prompt}'")
        result = pipeline.optimize_prompt(prompt, task_type)
        
        if result:
            print("\nResults:")
            print(f"Original: {result.original_prompt}")
            print(f"Optimized: {result.optimized_prompt}")
            print(f"Improvement Score: {result.improvement_score:.2f}")
            print("-" * 50)
        else:
            print(f"Failed to optimize prompt: {prompt}")
    
    # Save performance stats
    stats = pipeline.save_performance_stats()
    print("\nPerformance Summary:")
    print(stats)
