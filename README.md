# Prompt Versions Manager 🚀

A delightful Python package for managing LLM prompts with versioning and i18n-style string management. Perfect for keeping your AI conversations organized and maintainable!

## Installation 📦

You can install the package directly from PyPI using pip:

```bash
pip install prompt-versions-manager
```

That's it! Now you can start using the package in your Python projects.

## Why Prompt Versions Manager?

Managing prompts for Large Language Models can quickly become messy. As your application grows, you might find yourself:

- Copy-pasting prompts across different files 📋
- Struggling to maintain consistent versions 🔄
- Manually handling string interpolation 🔧
- Losing track of prompt variations 😅

Prompt Versions Manager solves these problems by providing an elegant, i18n-inspired solution that makes prompt management a breeze!

## Use Cases 💡

### Multi-Model Prompt Management
Use versions to maintain model-specific prompts. For example:

```python
from prompt_versions_manager import PromptVersionsManager

p = PromptVersionsManager()

# GPT-4 specific prompt
gpt4_response = p.version("gpt4").t("system.role")

# Claude specific prompt
claude_response = p.version("claude").t("system.role")

# Llama2 specific prompt
llama_response = p.version("llama2").t("system.role")

# Get all versions for LLM scoring
versions = p.get_all_versions("system.role")
# Returns: [
#   {"version": "claude", "value": "You are Claude, an AI assistant..."},
#   {"version": "gpt4", "value": "You are GPT-4, a large language model..."},
#   {"version": "llama2", "value": "You are Llama 2, an open-source AI..."}
# ]
```

### Multiple Prompt Sets
Use named managers to handle different types of prompts in your project:

```python
# Setup managers for different use cases
chat = PromptVersionsManager.setup("chat")
email = PromptVersionsManager.setup("email")

# Chat prompts in prompts/chat/v1.json
chat.set("greeting", "Hey {name}! How can I help?")

# Email prompts in prompts/email/v1.json
email.set("welcome", "Dear {name}, Welcome aboard!")
```

Your `prompts` directory could look like:
```
prompts/
├── chat/
│   ├── v1.json
│   └── v2.json
├── email/
│   ├── v1.json
│   └── v2.json
└── default/
    └── v1.json
```

## Features ✨

- **Automatic Prompt Creation** - Just use prompts and they're automatically saved
- **Version Control** - Maintain different versions of your prompts
- **Variable Interpolation** - Use placeholders like `{name}` in your prompts
- **Named Managers** - Organize prompts by use case or feature
- **JSON Storage** - Simple, human-readable storage format
- **FastAPI Integration** - Ready-to-use REST endpoints for your prompts
- **Zero Configuration** - Works out of the box with sensible defaults

## Quick Start 🏃‍♂️

```python
from prompt_versions_manager import PromptVersionsManager

# Get the default prompt manager
p = PromptVersionsManager()

# Use prompts with variables
welcome = p.t("welcome.message.{name}", name="Alice")
# Creates and returns: "welcome.message.Alice"

# Update existing prompts
p.set("welcome.message", "Hello {name}! Welcome aboard!")
welcome = p.t("welcome.message", name="Alice")
# Returns: "Hello Alice! Welcome aboard!"

# Switch versions
complex_prompt = (p.version("v2")
                  .t("debug.code.{language}.{aspect}",
                     language="Python",
                     aspect="performance"))

# List all versions
versions = p.versions()  # ['v1', 'v2']

# Find all versions of a prompt
welcome_versions = p.versions_for("welcome.message")
```

## FastAPI Integration 🌐

```python
from fastapi import FastAPI
from prompt_versions_manager import PromptVersionsManager

app = FastAPI()
chat = PromptVersionsManager("chat")
email = PromptVersionsManager("email")

@app.get("/prompts/{manager}/{version}/{prompt_id}")
async def get_prompt(manager: str, version: str, prompt_id: str, **params):
    p = PromptVersionsManager(manager)
    return {"prompt": p.version(version).t(prompt_id, **params)}

@app.get("/versions/{manager}")
async def list_versions(manager: str):
    return {"versions": PromptVersionsManager(manager).versions()}
```

## Configuration 🛠️

Configure through environment variables:

```bash
export PROMPTS_DIR="./prompts"        # Base directory for all prompt managers
export PROMPT_VERSION="v1"            # Default version
```

## Directory Structure 📁

Each named manager gets its own subdirectory:

```
prompts/
├── chat/                # Chat prompts
│   ├── v1.json
│   └── v2.json
└── email/              # Email prompts
    ├── v1.json
    └── v2.json
```

Example `chat/v1.json`:
```json
{
  "greeting": "Hey {name}! How can I help?",
  "farewell": "Thanks {name}! Have a great day!"
}
```

## Contributing 🤝

We love contributions! Feel free to:

1. Fork the repository
2. Create a feature branch
3. Submit a pull request

## License 📄

MIT License - feel free to use this in your projects!
