# LLM-Based-Prompt-Tuning

An intelligent system for optimizing prompts using dual LLM architecture with automated evaluation and persistence.

## 🚀 Features

- **Dual-Model Architecture**: Uses two LLMs (mistral, llama2) for optimization
- **Advanced Prompt Engineering**: Role-based templates and context management
- **Comprehensive Evaluation**: BLEU, ROUGE, and semantic similarity metrics
- **Data Persistence**: SQLite-based storage for optimization results
- **Automated Testing**: Full test suite across different prompt categories
- **Performance Monitoring**: GPU usage and response time tracking

## 📋 Prerequisites

- Python 3.12+
- [Ollama](https://ollama.ai/)
- CUDA-capable GPU (recommended)
- Linux environment

## 🛠️ Installation

```bash
# Clone the repository
git clone <your-repo-url>
cd LLM_PROJECT

# Create and activate virtual environment
python -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Download required models
ollama pull mistral
ollama pull llama2
```

## 💻 Usage

```bash
# Run the optimization pipeline
python src/optimization/pipeline.py

# Run evaluation and generate reports
python src/evaluation/evaluation_pipeline.py

# Run all tests
python -m unittest discover -v
```

## 📁 Project Structure

```
LLM_PROJECT/
├── config/           # Configuration files
├── data/            # Data storage
├── src/
│   ├── config/      # Configuration management
│   ├── data_persistence/
│   ├── evaluation/  # Metrics & evaluation
│   ├── logging/     # Performance monitoring
│   ├── models/      # Model interfaces
│   └── optimization/# Core optimization
└── tests/
    ├── integration/
    ├── prompt_suite/
    └── unit/
```

## ⚙️ Configuration

Edit files in `config/`:
- `config.yaml`: Main configuration
- `templates.yaml`: Prompt templates

## 📊 Evaluation

Results are saved in:
- `evaluation_results.csv`
- `evaluation_results.md`

## 📖 Documentation

See `docs/` for:
- Project roadmap
- Architecture decisions
- Performance benchmarks

## 🧪 Testing

```bash
# Run specific test suites
python -m unittest tests/prompt_suite/test_prompt_categories.py
python -m unittest tests/integration/test_database.py
```

## 📜 License

[MIT](LICENSE)

## 🤝 Contributing

Pull requests are welcome! Please open an issue first to discuss proposed changes.
