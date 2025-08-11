import json
from pathlib import Path
from typing import Dict, List, Optional
from datetime import datetime
from ..data_structures.schemas import OptimizationResult

class StorageManager:
    def __init__(self, base_path: str = "data"):
        self.base_path = Path(base_path)
        self.prompts_path = self.base_path / "prompts"
        self.responses_path = self.base_path / "responses"
        self._init_directories()
        
    def _init_directories(self):
        """Create necessary directories"""
        self.prompts_path.mkdir(parents=True, exist_ok=True)
        self.responses_path.mkdir(parents=True, exist_ok=True)
    
    def save_optimization_result(self, result: OptimizationResult):
        """Save optimization result"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")  # Added microseconds for uniqueness
        filename = f"optimization_{timestamp}.json"
        
        data = {
            "original_prompt": result.original_prompt,
            "optimized_prompt": result.optimized_prompt,
            "initial_response": result.initial_response,
            "final_response": result.final_response,
            "improvement_score": result.improvement_score,
            "created_at": result.created_at.isoformat(),
            "metadata": result.metadata or {}
        }
        
        with open(self.responses_path / filename, 'w') as f:
            json.dump(data, f, indent=2)
            
    def load_recent_results(self, limit: int = 10) -> List[OptimizationResult]:
        """Load recent optimization results"""
        # Get all optimization files
        files = list(self.responses_path.glob("optimization_*.json"))
        
        # Sort by filename (which contains timestamp)
        files.sort(reverse=True)
        
        # Take only the requested number of files
        files = files[:limit]
        
        results = []
        for file in files:
            try:
                with open(file) as f:
                    data = json.load(f)
                    results.append(OptimizationResult(
                        original_prompt=data["original_prompt"],
                        optimized_prompt=data["optimized_prompt"],
                        initial_response=data["initial_response"],
                        final_response=data["final_response"],
                        improvement_score=float(data["improvement_score"]),
                        created_at=datetime.fromisoformat(data["created_at"]),
                        metadata=data.get("metadata", {})
                    ))
            except Exception as e:
                print(f"Error loading file {file}: {e}")
                continue
                
        return results
