from typing import Dict, List, Optional
import numpy as np
from dataclasses import dataclass
from datetime import datetime
from nltk.translate.bleu_score import sentence_bleu
from rouge_score import rouge_scorer
from sentence_transformers import SentenceTransformer, util

# Load once at module level for efficiency
_sbert_model = SentenceTransformer('all-MiniLM-L6-v2')

def calculate_semantic_similarity(reference: str, hypothesis: str) -> float:
    """Compute cosine similarity between reference and hypothesis using SBERT."""
    emb1 = _sbert_model.encode(reference, convert_to_tensor=True)
    emb2 = _sbert_model.encode(hypothesis, convert_to_tensor=True)
    return float(util.pytorch_cos_sim(emb1, emb2).item())

def calculate_bleu(reference: str, hypothesis: str) -> float:
    return sentence_bleu([reference.split()], hypothesis.split())

def calculate_rouge(reference: str, hypothesis: str) -> dict:
    scorer = rouge_scorer.RougeScorer(['rouge1', 'rougeL'], use_stemmer=True)
    return scorer.score(reference, hypothesis)

@dataclass
class EvaluationMetrics:
    prompt_length: int
    response_length: int
    improvement_ratio: float
    coherence_score: float
    task_completion: float
    timestamp: datetime = datetime.now()

class MetricsCalculator:
    def __init__(self):
        self.metrics_history: List[EvaluationMetrics] = []
        
    def calculate_metrics(self, 
                         original_prompt: str,
                         optimized_prompt: str,
                         original_response: str,
                         optimized_response: str) -> EvaluationMetrics:
        """Calculate comprehensive evaluation metrics"""
        
        # Basic length metrics
        prompt_length = len(optimized_prompt) / len(original_prompt)
        response_length = len(optimized_response) / len(original_response)
        
        # Calculate improvement ratio
        improvement_ratio = response_length * 1.5 if response_length > 1 else response_length
        
        # Basic coherence check (can be enhanced with NLP libraries)
        coherence_score = self._calculate_coherence(optimized_response)
        
        # Task completion estimation
        task_completion = self._estimate_task_completion(
            optimized_prompt,
            optimized_response
        )
        
        metrics = EvaluationMetrics(
            prompt_length=prompt_length,
            response_length=response_length,
            improvement_ratio=improvement_ratio,
            coherence_score=coherence_score,
            task_completion=task_completion
        )
        
        self.metrics_history.append(metrics)
        return metrics
        
    def _calculate_coherence(self, text: str) -> float:
        """Calculate basic coherence score"""
        sentences = text.split('.')
        if len(sentences) < 2:
            return 0.5
            
        # Basic coherence heuristics
        avg_sentence_length = np.mean([len(s.split()) for s in sentences])
        length_variance = np.std([len(s.split()) for s in sentences])
        
        # Normalize scores
        length_score = min(avg_sentence_length / 20, 1.0)  # Assume 20 words is optimal
        variance_score = max(1 - (length_variance / avg_sentence_length), 0)
        
        return (length_score + variance_score) / 2
        
    def _estimate_task_completion(self, prompt: str, response: str) -> float:
        """Estimate if response completes the task from prompt"""
        prompt_keywords = set(prompt.lower().split())
        response_keywords = set(response.lower().split())
        
        # Calculate keyword overlap
        overlap = len(prompt_keywords.intersection(response_keywords))
        coverage = overlap / len(prompt_keywords) if prompt_keywords else 0
        
        return min(coverage * 1.5, 1.0)  # Scale up but cap at 1.0
        
    def get_summary_statistics(self) -> Dict:
        """Get summary statistics of all metrics"""
        if not self.metrics_history:
            return {}
            
        metrics_array = np.array([
            [m.improvement_ratio, m.coherence_score, m.task_completion]
            for m in self.metrics_history
        ])
        
        return {
            "avg_improvement": float(np.mean(metrics_array[:, 0])),
            "avg_coherence": float(np.mean(metrics_array[:, 1])),
            "avg_task_completion": float(np.mean(metrics_array[:, 2])),
            "overall_score": float(np.mean(metrics_array.mean(axis=1)))
        }
