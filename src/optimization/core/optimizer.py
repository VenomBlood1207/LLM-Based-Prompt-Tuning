from typing import Dict, List, Optional
from datetime import datetime
import logging

from ...data_structures.schemas import OptimizationResult
from ...models.ollama_api import OllamaAPI
from ...logging.monitor import PerformanceMonitor
from ..prompt_engineer import PromptEngineer

class OptimizationLoop:
    def __init__(self, config: Dict):
        self.config = config
        self.logger = logging.getLogger(__name__)
        self.monitor = PerformanceMonitor(config)
        self.prompt_engineer = PromptEngineer()
        self.model1 = OllamaAPI()
        self.model2 = OllamaAPI()
        
    def optimize_prompt(self, 
                       prompt: str, 
                       task_type: str = None,
                       max_iterations: int = 3,
                       improvement_threshold: float = 0.1) -> OptimizationResult:
        """Run the optimization loop"""
        
        start_time = datetime.now()
        current_prompt = prompt
        best_score = 0.0
        best_result = None
        
        for iteration in range(max_iterations):
            self.logger.info(f"Optimization iteration {iteration + 1}")
            
            # Get current response
            response = self.model1.generate_response(
                model=self.config["models"]["model1"]["name"],
                prompt=current_prompt
            )
            
            if not response:
                break
                
            # Generate optimization suggestions
            optimization_result = self.model2.generate_response(
                model=self.config["models"]["model2"]["name"],
                prompt=self._create_optimization_prompt(
                    current_prompt,
                    response["response"]
                )
            )
            
            if not optimization_result:
                break
                
            # Try optimized prompt
            new_prompt = optimization_result["response"]
            new_response = self.model1.generate_response(
                model=self.config["models"]["model1"]["name"],
                prompt=new_prompt
            )
            
            # Calculate improvement
            score = self._calculate_improvement(
                original_response=response["response"],
                new_response=new_response["response"]
            )
            
            # Update if better
            if score > best_score + improvement_threshold:
                best_score = score
                current_prompt = new_prompt
                best_result = OptimizationResult(
                    original_prompt=prompt,
                    optimized_prompt=new_prompt,
                    initial_response=response["response"],
                    final_response=new_response["response"],
                    improvement_score=score,
                    created_at=datetime.now(),
                    metadata={
                        "iterations": iteration + 1,
                        "duration": (datetime.now() - start_time).total_seconds()
                    }
                )
            else:
                break
                
        return best_result or OptimizationResult(
            original_prompt=prompt,
            optimized_prompt=prompt,
            initial_response=response["response"],
            final_response=response["response"],
            improvement_score=0.0,
            created_at=datetime.now(),
            metadata={"iterations": 0}
        )
        
    def _create_optimization_prompt(self, prompt: str, response: str) -> str:
        return self.prompt_engineer.enhance_prompt(
            original_prompt=prompt,
            task_type=None,  # Task type can be inferred or set explicitly
            model_response=response
        )
        
    def _calculate_improvement(self, 
                             original_response: str, 
                             new_response: str) -> float:
        # TODO: Implement sophisticated metrics
        return len(new_response) / len(original_response)
