# LLM Prompt Optimization System

An intelligent system that automatically optimizes prompts using dual LLM architecture.

## Project Overview

This system uses two Large Language Models working in tandem:
- **Model1**: Task executor that generates responses to prompts
- **Model2**: Prompt optimizer that analyzes and improves prompts

## Current Status

- [x] Day 1: Environment setup and model testing
- [x] Day 2: Model benchmarking and optimization
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

