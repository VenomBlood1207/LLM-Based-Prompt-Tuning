from typing import Dict, List
import statistics
from datetime import datetime

class PerformanceMetrics:
    def __init__(self):
        self.metrics = {
            "response_times": [],
            "improvement_scores": [],
            "success_rate": [],
            "memory_usage": []
        }
        
    def add_metric(self, category: str, value: float):
        """Add a metric measurement"""
        if category in self.metrics:
            self.metrics[category].append(value)
            
    def get_summary(self) -> Dict:
        """Get performance summary"""
        return {
            "avg_response_time": statistics.mean(self.metrics["response_times"]) if self.metrics["response_times"] else 0,
            "avg_improvement": statistics.mean(self.metrics["improvement_scores"]) if self.metrics["improvement_scores"] else 0,
            "success_rate": statistics.mean(self.metrics["success_rate"]) if self.metrics["success_rate"] else 0,
            "peak_memory": max(self.metrics["memory_usage"]) if self.metrics["memory_usage"] else 0
        }
