import logging
import time
from typing import Dict, Optional
import psutil
import json
from pathlib import Path
try:
    import nvidia_smi
    GPU_AVAILABLE = True
except ImportError:
    GPU_AVAILABLE = False

from ..data_structures.schemas import OptimizationResult

class PerformanceMonitor:
    def __init__(self, config: Dict):
        self.config = config
        self.logger = logging.getLogger(__name__)
        if GPU_AVAILABLE:
            nvidia_smi.nvmlInit()
        
        self.stats = {
            "gpu_usage": [],
            "memory_usage": [],
            "response_times": [],
            "optimization_success": 0,
            "optimization_failure": 0
        }
    
    def log_optimization(self, result: OptimizationResult):
        """Log optimization result"""
        if result and result.improvement_score > 0:
            self.stats["optimization_success"] += 1
        else:
            self.stats["optimization_failure"] += 1
        
        # Log GPU usage if available
        if GPU_AVAILABLE:
            try:
                handle = nvidia_smi.nvmlDeviceGetHandleByIndex(0)
                info = nvidia_smi.nvmlDeviceGetMemoryInfo(handle)
                self.stats["gpu_usage"].append(info.used / info.total)
            except Exception as e:
                self.logger.warning(f"Failed to log GPU usage: {e}")
            
    def log_performance(self, duration: float, memory_used: int):
        """Log performance metrics"""
        self.stats["response_times"].append(duration)
        self.stats["memory_usage"].append(memory_used)
        
    def save_stats(self):
        """Save statistics to file"""
        log_path = Path("logs/performance.json")
        log_path.parent.mkdir(exist_ok=True)
        
        with open(log_path, "w") as f:
            json.dump(self.stats, f, indent=2)
    
    def get_summary(self) -> Dict:
        """Get performance summary"""
        summary = {
            "avg_response_time": sum(self.stats["response_times"]) / len(self.stats["response_times"]) if self.stats["response_times"] else 0,
            "max_memory_usage": max(self.stats["memory_usage"]) if self.stats["memory_usage"] else 0,
            "success_rate": self.stats["optimization_success"] / (self.stats["optimization_success"] + self.stats["optimization_failure"]) if (self.stats["optimization_success"] + self.stats["optimization_failure"]) > 0 else 0
        }
        
        if GPU_AVAILABLE and self.stats["gpu_usage"]:
            summary["avg_gpu_usage"] = sum(self.stats["gpu_usage"]) / len(self.stats["gpu_usage"])
            summary["max_gpu_usage"] = max(self.stats["gpu_usage"])
            
        return summary

    def __del__(self):
        if GPU_AVAILABLE:
            try:
                nvidia_smi.nvmlShutdown()
            except:
                pass
