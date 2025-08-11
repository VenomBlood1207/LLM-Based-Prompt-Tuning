#!/usr/bin/env python3
"""
Advanced model testing for prompt optimization system
Tests model performance across different prompt types and scenarios
"""

import requests
import json
import time
import statistics
from typing import Dict, List, Tuple
import threading
from concurrent.futures import ThreadPoolExecutor
import logging

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class AdvancedModelTester:
    def __init__(self, base_url="http://localhost:11434"):
        self.base_url = base_url
        self.results = {}
        
        # Test prompt categories
        self.test_prompts = {
            "creative": [
                "Write a short story about a robot learning to paint.",
                "Create a poem about the ocean at sunset.",
                "Describe a futuristic city in vivid detail."
            ],
            "technical": [
                "Explain how machine learning works in simple terms.",
                "What are the key principles of software architecture?",
                "Describe the process of database normalization."
            ],
            "analytical": [
                "Compare the advantages and disadvantages of renewable energy.",
                "Analyze the impact of social media on modern communication.",
                "What are the main factors affecting climate change?"
            ],
            "instruction": [
                "Provide step-by-step instructions for making coffee.",
                "How do you troubleshoot a computer that won't start?",
                "Explain how to solve a quadratic equation."
            ],
            "conversational": [
                "What's your opinion on the future of artificial intelligence?",
                "How would you explain quantum physics to a child?",
                "What advice would you give to someone starting their career?"
            ]
        }
    
    def generate_response(self, model: str, prompt: str, params: Dict = None) -> Dict:
        """Generate response from a model with timing and error handling"""
        if params is None:
            params = {"temperature": 0.7, "top_p": 0.9}
        
        start_time = time.time()
        
        try:
            response = requests.post(
                f"{self.base_url}/api/generate",
                json={
                    "model": model,
                    "prompt": prompt,
                    "stream": False,
                    **params
                },
                timeout=120
            )
            
            response_time = time.time() - start_time
            
            if response.status_code == 200:
                data = response.json()
                return {
                    "success": True,
                    "response": data.get("response", ""),
                    "response_time": response_time,
                    "total_duration": data.get("total_duration", 0) / 1e9,  # Convert to seconds
                    "load_duration": data.get("load_duration", 0) / 1e9,
                    "prompt_eval_count": data.get("prompt_eval_count", 0),
                    "eval_count": data.get("eval_count", 0)
                }
            else:
                return {
                    "success": False,
                    "error": f"HTTP {response.status_code}",
                    "response_time": response_time
                }
                
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "response_time": time.time() - start_time
            }
    
    def test_model_categories(self, model: str) -> Dict:
        """Test model performance across different prompt categories"""
        logger.info(f"Testing {model} across prompt categories...")
        
        category_results = {}
        
        for category, prompts in self.test_prompts.items():
            logger.info(f"  Testing {category} prompts...")
            category_results[category] = []
            
            for prompt in prompts:
                result = self.generate_response(model, prompt)
                if result["success"]:
                    # Calculate quality metrics
                    response_text = result["response"]
                    quality_metrics = self.calculate_quality_metrics(prompt, response_text)
                    result.update(quality_metrics)
                
                category_results[category].append(result)
                time.sleep(1)  # Brief pause between requests
        
        # Calculate category summaries
        category_summaries = {}
        for category, results in category_results.items():
            successful_results = [r for r in results if r["success"]]
            if successful_results:
                category_summaries[category] = {
                    "success_rate": len(successful_results) / len(results),
                    "avg_response_time": statistics.mean([r["response_time"] for r in successful_results]),
                    "avg_response_length": statistics.mean([r["response_length"] for r in successful_results]),
                    "avg_quality_score": statistics.mean([r["quality_score"] for r in successful_results])
                }
            else:
                category_summaries[category] = {"success_rate": 0}
        
        return {
            "detailed_results": category_results,
            "category_summaries": category_summaries
        }
    
    def calculate_quality_metrics(self, prompt: str, response: str) -> Dict:
        """Calculate basic quality metrics for a response"""
        response_length = len(response)
        word_count = len(response.split())
        
        # Simple quality heuristics
        relevance_score = 1.0  # Placeholder - would need NLP libraries for real scoring
        completeness_score = min(1.0, word_count / 50)  # Assumes 50+ words is complete
        clarity_score = 1.0 - (response.count("unclear") + response.count("I don't know")) * 0.2
        
        quality_score = (relevance_score + completeness_score + clarity_score) / 3
        
        return {
            "response_length": response_length,
            "word_count": word_count,
            "quality_score": max(0.0, min(1.0, quality_score))
        }
    
    def test_concurrent_performance(self, model1: str, model2: str, iterations: int = 5) -> Dict:
        """Test concurrent model performance with multiple iterations"""
        logger.info(f"Testing concurrent performance: {model1} + {model2}")
        
        concurrent_results = []
        
        for i in range(iterations):
            logger.info(f"  Iteration {i+1}/{iterations}")
            
            # Different prompts for each iteration
            prompt1 = self.test_prompts["technical"][i % len(self.test_prompts["technical"])]
            prompt2 = self.test_prompts["analytical"][i % len(self.test_prompts["analytical"])]
            
            start_time = time.time()
            
            # Run both models concurrently
            with ThreadPoolExecutor(max_workers=2) as executor:
                future1 = executor.submit(self.generate_response, model1, prompt1)
                future2 = executor.submit(self.generate_response, model2, prompt2)
                
                result1 = future1.result()
                result2 = future2.result()
            
            total_time = time.time() - start_time
            
            concurrent_results.append({
                "iteration": i + 1,
                "total_time": total_time,
                "model1_success": result1["success"],
                "model2_success": result2["success"],
                "model1_time": result1["response_time"],
                "model2_time": result2["response_time"],
                "both_successful": result1["success"] and result2["success"]
            })
            
            time.sleep(2)  # Cool down between iterations
        
        # Calculate summary statistics
        successful_runs = [r for r in concurrent_results if r["both_successful"]]
        
        if successful_runs:
            summary = {
                "success_rate": len(successful_runs) / len(concurrent_results),
                "avg_total_time": statistics.mean([r["total_time"] for r in successful_runs]),
                "avg_model1_time": statistics.mean([r["model1_time"] for r in successful_runs]),
                "avg_model2_time": statistics.mean([r["model2_time"] for r in successful_runs]),
                "max_total_time": max([r["total_time"] for r in successful_runs]),
                "min_total_time": min([r["total_time"] for r in successful_runs])
            }
        else:
            summary = {"success_rate": 0}
        
        return {
            "detailed_results": concurrent_results,
            "summary": summary
        }
    
    def test_parameter_optimization(self, model: str) -> Dict:
        """Test different parameter combinations for optimal performance"""
        logger.info(f"Testing parameter optimization for {model}")
        
        parameter_sets = [
            {"temperature": 0.3, "top_p": 0.8, "name": "conservative"},
            {"temperature": 0.7, "top_p": 0.9, "name": "balanced"},
            {"temperature": 1.0, "top_p": 0.95, "name": "creative"},
            {"temperature": 0.1, "top_p": 0.5, "name": "deterministic"}
        ]
        
        test_prompt = "Explain the concept of machine learning and provide a practical example."
        parameter_results = {}
        
        for params in parameter_sets:
            name = params.pop("name")
            logger.info(f"  Testing {name} parameters...")
            
            # Test multiple times for consistency
            results = []
            for _ in range(3):
                result = self.generate_response(model, test_prompt, params)
                if result["success"]:
                    quality_metrics = self.calculate_quality_metrics(test_prompt, result["response"])
                    result.update(quality_metrics)
                results.append(result)
            
            # Calculate averages
            successful_results = [r for r in results if r["success"]]
            if successful_results:
                parameter_results[name] = {
                    "success_rate": len(successful_results) / len(results),
                    "avg_response_time": statistics.mean([r["response_time"] for r in successful_results]),
                    "avg_quality": statistics.mean([r["quality_score"] for r in successful_results]),
                    "avg_length": statistics.mean([r["response_length"] for r in successful_results]),
                    "sample_response": successful_results[0]["response"][:200] + "..."
                }
        
        return parameter_results
    
    def run_comprehensive_test(self):
        """Run all tests for the optimal model combination"""
        models_to_test = ["mistral:7b", "llama3.2:3b", "phi3:3.8b"]
        
        # Add llama3.1:8b if it's working now
        test_result = self.generate_response("llama3.1:8b", "Hello, test message.")
        if test_result["success"]:
            models_to_test.append("llama3.1:8b")
            logger.info("✓ llama3.1:8b is now working!")
        else:
            logger.warning("✗ llama3.1:8b still not working")
        
        logger.info("Starting comprehensive model testing...")
        logger.info(f"Testing models: {models_to_test}")
        
        # Test individual model performance across categories
        for model in models_to_test:
            logger.info(f"\n{'='*50}")
            logger.info(f"TESTING {model.upper()}")
            logger.info(f"{'='*50}")
            
            self.results[model] = {}
            
            # Category testing
            self.results[model]["categories"] = self.test_model_categories(model)
            
            # Parameter optimization
            self.results[model]["parameters"] = self.test_parameter_optimization(model)
        
        # Test optimal concurrent combinations
        concurrent_combinations = [
            ("mistral:7b", "llama3.2:3b"),
            ("mistral:7b", "phi3:3.8b")
        ]
        
        if "llama3.1:8b" in models_to_test:
            concurrent_combinations.extend([
                ("llama3.1:8b", "llama3.2:3b"),
                ("llama3.1:8b", "phi3:3.8b")
            ])
        
        self.results["concurrent_tests"] = {}
        for model1, model2 in concurrent_combinations:
            combo_name = f"{model1}+{model2}"
            logger.info(f"\n{'='*50}")
            logger.info(f"TESTING CONCURRENT: {combo_name.upper()}")
            logger.info(f"{'='*50}")
            
            self.results["concurrent_tests"][combo_name] = self.test_concurrent_performance(model1, model2)

    def generate_recommendations(self):
        """Generate recommendations based on test results"""
        logger.info("\n" + "="*60)
        logger.info("COMPREHENSIVE TEST RESULTS & RECOMMENDATIONS")
        logger.info("="*60)
        
        # Find best individual models for each role
        model1_candidates = []  # Task executors
        model2_candidates = []  # Prompt optimizers
        
        for model, results in self.results.items():
            if model == "concurrent_tests":
                continue
                
            if "categories" in results:
                summaries = results["categories"]["category_summaries"]
                
                # Calculate overall score
                scores = []
                for category, summary in summaries.items():
                    if "avg_quality_score" in summary:
                        scores.append(summary["avg_quality_score"])
                
                if scores:
                    overall_score = statistics.mean(scores)
                    
                    # Classify based on model size and performance
                    if "7b" in model or "mistral" in model:
                        model1_candidates.append((model, overall_score))
                    else:
                        model2_candidates.append((model, overall_score))
        
        # Sort by performance
        model1_candidates.sort(key=lambda x: x[1], reverse=True)
        model2_candidates.sort(key=lambda x: x[1], reverse=True)
        
        logger.info("\nMODEL RECOMMENDATIONS:")
        logger.info("-" * 30)
        
        if model1_candidates:
            best_model1 = model1_candidates[0][0]
            logger.info(f"Recommended Model1 (Task Executor): {best_model1}")
            logger.info(f"  Score: {model1_candidates[0][1]:.3f}")
        
        if model2_candidates:
            best_model2 = model2_candidates[0][0]
            logger.info(f"Recommended Model2 (Prompt Optimizer): {best_model2}")
            logger.info(f"  Score: {model2_candidates[0][1]:.3f}")
        
        # Analyze concurrent performance
        if "concurrent_tests" in self.results:
            logger.info(f"\nCONCURRENT PERFORMANCE:")
            logger.info("-" * 30)
            
            concurrent_scores = []
            for combo, results in self.results["concurrent_tests"].items():
                if "summary" in results and "success_rate" in results["summary"]:
                    success_rate = results["summary"]["success_rate"]
                    avg_time = results["summary"].get("avg_total_time", float('inf'))
                    
                    # Combined score: prioritize success rate, then speed
                    combined_score = success_rate * (1 / (avg_time + 1))
                    concurrent_scores.append((combo, success_rate, avg_time, combined_score))
            
            concurrent_scores.sort(key=lambda x: x[3], reverse=True)
            
            for combo, success_rate, avg_time, score in concurrent_scores[:3]:
                logger.info(f"{combo}:")
                logger.info(f"  Success Rate: {success_rate:.1%}")
                logger.info(f"  Avg Time: {avg_time:.2f}s")
                logger.info(f"  Combined Score: {score:.3f}")
                logger.info(" ")  # Changed from logger.info() to logger.info(" ")
        
        # Save detailed results
        with open("data/benchmarks/advanced_test_results.json", "w") as f:
            json.dump(self.results, f, indent=2)
        
        logger.info("Detailed results saved to: data/benchmarks/advanced_test_results.json")

if __name__ == "__main__":
    tester = AdvancedModelTester()
    
    # Test connectivity
    try:
        response = requests.get("http://localhost:11434/api/tags", timeout=5)
        if response.status_code != 200:
            logger.error("Cannot connect to Ollama. Make sure it's running.")
            exit(1)
    except:
        logger.error("Cannot connect to Ollama. Make sure it's running.")
        exit(1)
    
    logger.info("Starting advanced model testing...")
    tester.run_comprehensive_test()
    tester.generate_recommendations()
    logger.info("Advanced testing complete!")
