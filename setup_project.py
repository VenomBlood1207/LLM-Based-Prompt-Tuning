#!/usr/bin/env python3
"""
Project setup script for LLM Prompt Optimization System
Creates directory structure and initial configuration files
"""

import os
import json
from pathlib import Path

def create_project_structure():
    """Create the project directory structure"""
    
    # Define project structure
    directories = [
        "src",
        "src/models",
        "src/optimization",
        "src/evaluation", 
        "src/utils",
        "src/interfaces",
        "data",
        "data/prompts",
        "data/responses", 
        "data/benchmarks",
        "config",
        "logs",
        "tests",
        "tests/unit",
        "tests/integration",
        "docs",
        "experiments",
        "exports"
    ]
    
    # Create directories
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"Created directory: {directory}")
    
    # Create initial configuration files
    create_config_files()
    create_requirements_file()
    create_gitignore()
    create_readme()
    
    print("\n✓ Project structure created successfully!")

def create_config_files():
    """Create initial configuration files"""
    
    # Main configuration
    main_config = {
        "system": {
            "ollama_url": "http://localhost:11434",
            "max_retries": 3,
            "timeout": 120,
            "log_level": "INFO"
        },
        "models": {
            "model1": {
                "name": "llama3.2:7b",
                "role": "task_executor",
                "parameters": {
                    "temperature": 0.7,
                    "top_p": 0.9,
                    "max_tokens": 2048
                }
            },
            "model2": {
                "name": "llama3.2:3b", 
                "role": "prompt_optimizer",
                "parameters": {
                    "temperature": 0.3,
                    "top_p": 0.8,
                    "max_tokens": 512
                }
            }
        },
        "optimization": {
            "max_iterations": 3,
            "improvement_threshold": 0.1,
            "evaluation_metrics": ["bleu", "rouge", "semantic_similarity"],
            "save_intermediate_results": True
        },
        "evaluation": {
            "batch_size": 10,
            "human_evaluation": False,
            "auto_save_results": True
        }
    }
    
    with open("config/main_config.json", "w") as f:
        json.dump(main_config, f, indent=2)
    
    # Model-specific configurations
    model_configs = {
        "llama3.2:7b": {
            "context_length": 4096,
            "memory_requirement": "~6GB",
            "strengths": ["reasoning", "general_knowledge", "creative_writing"],
            "optimal_use_cases": ["complex_tasks", "long_context", "detailed_responses"]
        },
        "llama3.2:3b": {
            "context_length": 4096,
            "memory_requirement": "~2GB", 
            "strengths": ["efficiency", "quick_responses", "prompt_analysis"],
            "optimal_use_cases": ["prompt_optimization", "quick_analysis", "classification"]
        },
        "mistral:7b": {
            "context_length": 8192,
            "memory_requirement": "~6GB",
            "strengths": ["coding", "technical_content", "structured_output"],
            "optimal_use_cases": ["code_generation", "technical_writing", "analysis"]
        },
        "phi3:3.8b": {
            "context_length": 4096,
            "memory_requirement": "~2.5GB",
            "strengths": ["reasoning", "mathematics", "compact_responses"],
            "optimal_use_cases": ["logical_tasks", "optimization", "brief_analysis"]
        }
    }
    
    with open("config/model_configs.json", "w") as f:
        json.dump(model_configs, f, indent=2)
    
    print("Created configuration files")

def create_requirements_file():
    """Create requirements.txt file"""
    requirements = [
        "requests>=2.31.0",
        "numpy>=1.24.0",
        "pandas>=2.0.0",
        "scikit-learn>=1.3.0",
        "nltk>=3.8.0",
        "rouge-score>=0.1.2",
        "sentence-transformers>=2.2.0",
        "psutil>=5.9.0",
        "tqdm>=4.65.0",
        "click>=8.0.0",
        "colorama>=0.4.6",
        "python-dotenv>=1.0.0",
        "sqlalchemy>=2.0.0",
        "fastapi>=0.100.0",
        "uvicorn>=0.22.0",
        "streamlit>=1.25.0",
        "plotly>=5.15.0",
        "seaborn>=0.12.0",
        "matplotlib>=3.7.0"
    ]
    
    with open("requirements.txt", "w") as f:
        f.write("\n".join(requirements))
    
    print("Created requirements.txt")

def create_gitignore():
    """Create .gitignore file"""
    gitignore_content = """# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Virtual Environment
venv/
env/
ENV/

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# Project specific
logs/*.log
data/responses/*.json
data/benchmarks/*.json
exports/*.json
experiments/*/results/
*.db
*.sqlite

# OS
.DS_Store
Thumbs.db

# Temporary files
*.tmp
*.temp
.cache/

# API Keys and secrets
.env
secrets.json
"""
    
    with open(".gitignore", "w") as f:
        f.write(gitignore_content)
    
    print("Created .gitignore")

def create_readme():
    """Create initial README.md"""
    readme_content = """# LLM Prompt Optimization System

An intelligent system that automatically optimizes prompts using dual LLM architecture.

## Project Overview

This system uses two Large Language Models working in tandem:
- **Model1**: Task executor that generates responses to prompts
- **Model2**: Prompt optimizer that analyzes and improves prompts

## Current Status

- [x] Day 1: Environment setup and model testing
- [ ] Day 2: Model benchmarking and optimization
- [ ] Day 3-4: Core architecture design
- [ ] Day 5-7: Initial implementation

## Quick Start

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Run model benchmarking:
   ```bash
   python model_memory_test.py
   ```

3. Check configuration:
   ```bash
   cat config/main_config.json
   ```

## Hardware Requirements

- Intel i7-14650HK processor
- 16GB RAM
- RTX 4060 GPU (8GB VRAM)
- Ollama runtime

## Project Structure

```
├── src/           # Source code
├── config/        # Configuration files
├── data/          # Data storage
├── logs/          # Log files
├── tests/         # Test files
├── docs/          # Documentation
└── experiments/   # Experimental code
```

## Next Steps

See the 30-day roadmap in the project documentation.
"""
    
    with open("README.md", "w") as f:
        f.write(readme_content)
    
    print("Created README.md")

if __name__ == "__main__":
    print("Setting up LLM Prompt Optimization Project...")
    print("=" * 50)
    create_project_structure()
    print("\nProject setup complete! Next steps:")
    print("1. Run: python model_memory_test.py")
    print("2. Review config/main_config.json")
    print("3. Install requirements: pip install -r requirements.txt")
