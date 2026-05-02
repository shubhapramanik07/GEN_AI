# GEN_AI - Generative AI Integration Project

A Python project for building generative AI applications with LangChain integrations supporting multiple LLM providers including OpenAI, Hugging Face, and Mistral.

## Features

- **Multi-Provider LLM Support**
  - OpenAI (GPT models)
  - Hugging Face Hub
  - Mistral AI
- **Chat Models** - Interactive LLM interfaces for conversation and Q&A
- **Embedding Models** - Text embedding generation and processing
- **Easy Configuration** - Environment-based API key management
- **Extensible Architecture** - Modular design for adding new providers

## Prerequisites

- Python 3.10 or higher
- pip or uv package manager
- API keys for the providers you want to use:
  - [OpenAI API Key](https://platform.openai.com/api-keys)
  - [Hugging Face Hub Token](https://huggingface.co/settings/tokens)
  - [Mistral API Key](https://console.mistral.ai/)

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/shubhapramanik07/GEN_AI.git
cd GEN_AI
```

### 2. Create Virtual Environment

```bash
# Using venv
python -m venv .venv

# Activate virtual environment
# On Windows:
.venv\Scripts\activate
# On macOS/Linux:
source .venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

Or using uv:

```bash
uv pip install -r requirements.txt
```

### 4. Setup Environment Variables

Create a `.env` file in the project root and add your API keys:

```env
OPENAI_API_KEY=your_openai_api_key_here
HUGGINGFACEHUB_API_TOKEN=your_huggingface_token_here
MISTRAL_API_KEY=your_mistral_api_key_here
```

**⚠️ Security Note:** Never commit `.env` file to version control. It's included in `.gitignore`.

## Project Structure

```
GEN_AI/
├── chatmodels/
│   ├── chat.py              # LangChain chat model initialization
│   ├── huggingface.py       # Hugging Face integration example
│   └── localmodel.py        # Local model examples
├── embeddingmodels/
│   └── embeddings.py        # Embedding model implementations
├── requirements.txt         # Project dependencies
├── pyproject.toml          # Project metadata
├── .env.example            # Example environment variables (template)
├── .gitignore              # Git ignore rules
└── README.md               # This file
```

## Usage

### OpenAI Chat Model

```python
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

load_dotenv()

llm = ChatOpenAI(model="gpt-4", temperature=0.7)
response = llm.invoke("What is the capital of France?")
print(response)
```

### Hugging Face Integration

```python
from dotenv import load_dotenv
from langchain_huggingface import HuggingFaceHub

load_dotenv()

llm = HuggingFaceHub(repo_id="google/flan-t5-large")
response = llm("Translate English to French: Hello")
print(response)
```

### Mistral AI Integration

```python
from dotenv import load_dotenv
from langchain_mistralai.chat_models import ChatMistralAI

load_dotenv()

llm = ChatMistralAI(model="mistral-large-latest")
response = llm.invoke("Explain machine learning")
print(response)
```

### Running Examples

```bash
# Run OpenAI example
python chatmodels/huggingface.py

# Run chat model initialization
python chatmodels/chat.py

# Run local model
python chatmodels/localmodel.py

# Run embeddings
python embeddingmodels/embeddings.py
```

## Dependencies

- **langchain** - Framework for building with language models
- **langchain-openai** - OpenAI integration
- **langchain-huggingface** - Hugging Face integration
- **langchain-mistralai** - Mistral AI integration
- **python-dotenv** - Environment variable management
- **huggingface-hub** - Hugging Face Hub API client

For full dependency list, see [requirements.txt](requirements.txt).

## Configuration

### Environment Variables

| Variable                   | Description                   | Example       |
| -------------------------- | ----------------------------- | ------------- |
| `OPENAI_API_KEY`           | OpenAI API key for GPT models | `sk-proj-...` |
| `HUGGINGFACEHUB_API_TOKEN` | Hugging Face Hub API token    | `hf_...`      |
| `MISTRAL_API_KEY`          | Mistral AI API key            | `mistral_...` |

Load environment variables in your code:

```python
from dotenv import load_dotenv
import os

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
```

## Troubleshooting

### ModuleNotFoundError: No module named 'langchain_openai'

Ensure all dependencies are installed:

```bash
pip install -r requirements.txt
```

### OpenAI API Error: Insufficient quota

Check your OpenAI account billing and quota limits at [platform.openai.com](https://platform.openai.com/account/billing/overview).

### Import Error with relative imports

When running scripts directly, use absolute paths or run as modules:

```bash
# Correct ways to run
python -m chatmodels.chat
python chatmodels/chat.py  # From project root

# Avoid
python ./chatmodels/chat.py  # From nested directory
```

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/your-feature`)
3. Commit changes (`git commit -m 'Add your feature'`)
4. Push to branch (`git push origin feature/your-feature`)
5. Open a Pull Request

## Security

- Never commit `.env` files or API keys to version control
- Rotate API keys regularly if exposed
- Use environment variables for all sensitive configuration
- Review LangChain's security documentation for best practices

## License

This project is open source and available under the MIT License.

## Resources

- [LangChain Documentation](https://python.langchain.com/)
- [OpenAI API Documentation](https://platform.openai.com/docs/)
- [Hugging Face Hub Documentation](https://huggingface.co/docs/hub/index)
- [Mistral AI Documentation](https://docs.mistral.ai/)

## Support

For issues, questions, or contributions, please open an issue on [GitHub](https://github.com/shubhapramanik07/GEN_AI/issues).

---

**Last Updated:** May 2, 2026
