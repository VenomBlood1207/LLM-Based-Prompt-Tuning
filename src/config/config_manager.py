import yaml
from pathlib import Path
from typing import Dict, Any

class ConfigManager:
    def __init__(self, config_path: str = "config/config.yaml"):
        self.config_path = Path(config_path)
        self.config = self._load_config()
        
    def _load_config(self) -> Dict[str, Any]:
        if not self.config_path.exists():
            self._create_default_config()
        
        with open(self.config_path) as f:
            return yaml.safe_load(f)
            
    def _create_default_config(self):
        default_config = {
            "models": {
                "model1": {
                    "name": "mistral",
                    "parameters": {
                        "temperature": 0.7,
                        "max_tokens": 2048
                    }
                },
                "model2": {
                    "name": "llama2",
                    "parameters": {
                        "temperature": 0.3,
                        "max_tokens": 512
                    }
                }
            },
            "optimization": {
                "max_iterations": 3,
                "improvement_threshold": 0.1,
                "timeout": 30
            },
            "logging": {
                "level": "INFO",
                "file": "logs/optimization.log",
                "performance_metrics": True
            }
        }
        
        self.config_path.parent.mkdir(exist_ok=True)
        with open(self.config_path, 'w') as f:
            yaml.dump(default_config, f, default_flow_style=False)
