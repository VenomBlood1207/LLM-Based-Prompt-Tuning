from dataclasses import dataclass
from typing import Dict, List, Optional
from datetime import datetime

@dataclass
class PromptResponse:
    prompt_id: str
    prompt_text: str
    response_text: str
    model_name: str
    created_at: datetime
    metadata: Dict
    quality_scores: Optional[Dict] = None

@dataclass
class OptimizationResult:
    original_prompt: str
    optimized_prompt: str
    initial_response: str
    final_response: str
    improvement_score: float
    created_at: datetime = datetime.now()
    metadata: Dict = None
