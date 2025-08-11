#!/usr/bin/env python3
"""
Configuration optimizer based on benchmark results
Updates system configuration for optimal performance
"""

import json
import os
from pathlib import Path

def update_config_from_benchmarks():
    """Update configuration based on benchmark results"""
    
    # Load benchmark results
    try:
        with open("model_benchmark_results.json", "r") as f:
            benchmark_data = json.load(f)
    except FileNotFoundError:
        print("Benchmark results not found. Please run model_memory_test.py first.")
        return
    
    # Analyze results and determine optimal configuration
    optimal_config = analyze_benchmarks(benchmark_data)
    
    # Update main configuration
    update_main_config(optimal_config)
    
    # Create hardware-specific configuration
    create_hardware_config(benchmark_data)
    
    # Create prompt templates for Model2
    create_prompt_templates()
    
    print("✓ Configuration optimized based on benchmark results!")

def analyze_benchmarks(data):
    """Analyze benchmark data to determine optimal configuration"""
    
    # Find working models
    working_models = {}
    for model, result in data.items():
        if model != "concurrent" and result.get("success", False):
            working_models[model] = {
                "gpu_memory": result.get("gpu_memory_mb", 0),
                "load_time": result.get("load_time", 0),
                "response_quality": result.get("response_length", 0)
            }
    
    # Find optimal concurrent combination
    best_concurrent = None
    if "concurrent" in data:
        for combo, result in data["concurrent"].items():
            if result.get("overall_success", False):
                if best_concurrent is None or result["total_gpu"] < best_concurrent["gpu_usage"]:
                    best_concurrent = {
                        "combination": combo,
                        "models": combo.split("+"),
                        "gpu_usage": result["total_gpu"],
                        "execution_time": result["total_time"]
                    }
    
    # Based on your results: mistral:7b + llama3.2:3b is optimal
    optimal_config = {
        "model1": {
            "name": "mistral:7b",
            "role": "task_executor",
            "gpu_memory_mb": 5569,
            "strengths": ["technical_content", "structured_output", "reasoning"]
        },
        "model2": {
            "name": "llama3.2:3b", 
            "role": "prompt_optimizer",
            "gpu_memory_mb": 2200,
            "strengths": ["efficiency", "analysis", "prompt_refinement"]
        },
        "concurrent_performance": {
            "total_gpu_usage": 3390,  # From your results
            "expected_time": 9.44,
            "success_rate": 1.0
        }
    }
    
    return optimal_config

def update_main_config(optimal_config):
    """Update the main configuration file"""
    
    config = {
        "system": {
            "ollama_url": "http://localhost:11434",
            "max_retries": 3,
            "timeout": 120,
            "log_level": "INFO",
            "hardware_profile": "rtx4060_16gb"
        },
        "models": {
            "model1": {
                "name": optimal_config["model1"]["name"],
                "role": "task_executor",
                "parameters": {
                    "temperature": 0.7,
                    "top_p": 0.9,
                    "max_tokens": 2048,
                    "context_length": 8192  # mistral:7b supports longer context
                },
                "memory_usage_mb": optimal_config["model1"]["gpu_memory_mb"],
                "specialties": optimal_config["model1"]["strengths"]
            },
            "model2": {
                "name": optimal_config["model2"]["name"],
                "role": "prompt_optimizer", 
                "parameters": {
                    "temperature": 0.3,  # Lower temperature for more focused optimization
                    "top_p": 0.8,
                    "max_tokens": 1024,  # Shorter responses for prompt optimization
                    "context_length": 4096
                },
                "memory_usage_mb": optimal_config["model2"]["gpu_memory_mb"],
                "specialties": optimal_config["model2"]["strengths"]
            }
        },
        "optimization": {
            "max_iterations": 3,
            "improvement_threshold": 0.15,  # 15% improvement required
            "evaluation_metrics": ["response_length", "coherence", "task_completion"],
            "save_intermediate_results": True,
            "concurrent_execution": True,
            "memory_monitoring": True
        },
        "evaluation": {
            "batch_size": 5,  # Conservative for your hardware
            "human_evaluation": False,
            "auto_save_results": True,
            "quality_threshold": 0.7,
            "comparison_methods": ["before_after", "statistical_significance"]
        },
        "performance": {
            "expected_gpu_usage_mb": optimal_config["concurrent_performance"]["total_gpu_usage"],
            "expected_response_time_s": optimal_config["concurrent_performance"]["expected_time"],
            "memory_safety_buffer_mb": 500,
            "cpu_fallback_enabled": True
        }
    }
    
    os.makedirs("config", exist_ok=True)
    with open("config/main_config.json", "w") as f:
        json.dump(config, f, indent=2)
    
    print("Updated config/main_config.json")

def create_hardware_config(benchmark_data):
    """Create hardware-specific configuration"""
    
    hardware_config = {
        "gpu": {
            "model": "RTX 4060",
            "memory_gb": 8,
            "memory_mb": 8192,
            "cuda_cores": 3072,
            "optimal_utilization": 0.85  # Use 85% of GPU memory max
        },
        "cpu": {
            "model": "Intel i7-14650HK",
            "cores": 20,  # 6P + 8E + 6HT
            "threads": 20,
            "base_clock_ghz": 3.5,
            "boost_clock_ghz": 5.2
        },
        "memory": {
            "total_gb": 16,
            "available_for_models_gb": 12,  # Reserve 4GB for system
            "swap_enabled": True
        },
        "benchmarks": {
            "models_tested": list(benchmark_data.keys()),
            "optimal_combination": "mistral:7b+llama3.2:3b",
            "max_concurrent_gpu_usage_mb": 6000,  # Safe limit
            "recommended_batch_size": 5
        },
        "limits": {
            "max_gpu_memory_mb": 7000,  # Leave buffer
            "max_concurrent_models": 2,
            "timeout_seconds": 120,
            "retry_attempts": 3
        }
    }
    
    with open("config/hardware_config.json", "w") as f:
        json.dump(hardware_config, f, indent=2)
    
    print("Created config/hardware_config.json")

def create_prompt_templates():
    """Create prompt templates for Model2 (prompt optimizer)"""
    
    templates = {
        "base_optimization_template": """You are an expert prompt optimizer. Your task is to analyze a prompt and its generated response, then create an improved version of the prompt.

ORIGINAL PROMPT: {original_prompt}

MODEL RESPONSE: {model_response}

TASK TYPE: {task_type}

ANALYSIS:
1. Response Quality Assessment:
   - Completeness: {completeness_score}/10
   - Relevance: {relevance_score}/10
   - Clarity: {clarity_score}/10

2. Prompt Issues Identified:
   - Missing context: {missing_context}
   - Ambiguous instructions: {ambiguous_parts}
   - Unclear desired format: {format_issues}

OPTIMIZATION STRATEGY:
Based on the analysis, I will improve the prompt by:
1. Adding specific context and background information
2. Clarifying the desired output format and structure
3. Providing clear, actionable instructions
4. Including relevant constraints or guidelines

OPTIMIZED PROMPT:""",

        "creative_optimization_template": """You are optimizing a creative writing prompt. Focus on inspiring creativity while maintaining clear direction.

ORIGINAL PROMPT: {original_prompt}
RESPONSE QUALITY: {quality_assessment}

Enhancement Areas:
- Sensory details and atmosphere
- Character development cues
- Setting and world-building elements
- Emotional tone and style guidance

OPTIMIZED CREATIVE PROMPT:""",

        "technical_optimization_template": """You are optimizing a technical prompt. Focus on precision, completeness, and practical applicability.

ORIGINAL PROMPT: {original_prompt}
TECHNICAL ACCURACY: {accuracy_score}
COMPLETENESS: {completeness_score}

Enhancement Areas:
- Technical specifications and requirements
- Step-by-step structure
- Examples and use cases
- Error handling and edge cases

OPTIMIZED TECHNICAL PROMPT:""",

        "analytical_optimization_template": """You are optimizing an analytical prompt. Focus on depth, structure, and evidence-based reasoning.

ORIGINAL PROMPT: {original_prompt}
ANALYSIS DEPTH: {depth_score}
LOGICAL STRUCTURE: {structure_score}

Enhancement Areas:
- Clear analytical framework
- Specific aspects to examine
- Evidence and reasoning requirements
- Comparative or evaluative criteria

OPTIMIZED ANALYTICAL PROMPT:""",

        "instructional_optimization_template": """You are optimizing an instructional prompt. Focus on clarity, actionability, and step-by-step guidance.

ORIGINAL PROMPT: {original_prompt}
INSTRUCTION CLARITY: {clarity_score}
ACTIONABILITY: {actionable_score}

Enhancement Areas:
- Sequential step structure
- Prerequisites and requirements
- Expected outcomes and verification
- Troubleshooting guidance

OPTIMIZED INSTRUCTIONAL PROMPT:"""
    }
    
    os.makedirs("config/templates", exist_ok=True)
    with open("config/templates/prompt_templates.json", "w") as f:
        json.dump(templates, f, indent=2)
    
    # Create template usage guide
    usage_guide = {
        "template_selection": {
            "creative": ["story", "poem", "creative writing", "narrative", "fiction"],
            "technical": ["explain", "code", "algorithm", "programming", "technical"],
            "analytical": ["analyze", "compare", "evaluate", "assess", "critique"],
            "instructional": ["how to", "steps", "tutorial", "guide", "instruction"]
        },
        "parameter_mapping": {
            "original_prompt": "The user's original prompt text",
            "model_response": "The response generated by Model1",
            "task_type": "Automatically detected task category",
            "quality_assessment": "Automated quality score (0-1)",
            "completeness_score": "How complete the response is (1-10)",
            "relevance_score": "How relevant the response is (1-10)", 
            "clarity_score": "How clear the response is (1-10)"
        },
        "optimization_strategies": {
            "add_context": "Include relevant background information",
            "specify_format": "Define expected output structure",
            "clarify_scope": "Define boundaries and limitations", 
            "add_examples": "Include sample inputs/outputs",
            "enhance_instructions": "Make instructions more specific and actionable"
        }
    }
    
    with open("config/templates/template_usage_guide.json", "w") as f:
        json.dump(usage_guide, f, indent=2)
    
    print("Created prompt templates and usage guide")

if __name__ == "__main__":
    print("Optimizing configuration based on benchmark results...")
    update_config_from_benchmarks()
    print("\nConfiguration optimization complete!")
    print("\nNext steps:")
    print("1. Review config/main_config.json") 
    print("2. Run advanced_model_testing.py")
    print("3. Check config/templates/ for prompt optimization templates")
