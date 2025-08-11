from typing import Dict, List, Optional
import yaml
from pathlib import Path

class PromptEngineer:
    def __init__(self, template_path: str = "config/templates.yaml"):
        self.template_path = Path(template_path)
        self.templates = self._load_templates()
        self.task_patterns = {
            "general": ["what is", "tell me about", "explain"],
            "technical": ["how does", "implement", "architecture"],
            "creative": ["write", "create", "design", "story"],
            "analytical": ["compare", "analyze", "evaluate"]
        }
        
    def _load_templates(self) -> Dict:
        """Load templates from YAML file"""
        if not self.template_path.exists():
            raise FileNotFoundError(f"Template file not found: {self.template_path}")
            
        with open(self.template_path) as f:
            return yaml.safe_load(f)
            
    def detect_task_type(self, prompt: str) -> str:
        """Detect task type from prompt"""
        prompt_lower = prompt.lower()
        
        for task_type, patterns in self.task_patterns.items():
            if any(pattern in prompt_lower for pattern in patterns):
                return task_type
                
        return "general"
        
    def enhance_prompt(self, original_prompt: str, task_type: Optional[str] = None, model_response: str = "", role: str = "") -> str:
        if task_type is None:
            task_type = self.detect_task_type(original_prompt)
        if task_type not in self.templates["task_types"]:
            task_type = "general"
        template = self.templates["task_types"][task_type]["template"]
        if task_type == "role" and role:
            enhanced = template.format(
                original_prompt=original_prompt,
                model_response=model_response,
                task_type=task_type,
                role=role
            )
        else:
            enhanced = template.format(
                original_prompt=original_prompt,
                model_response=model_response,
                task_type=task_type
            )
        return enhanced
