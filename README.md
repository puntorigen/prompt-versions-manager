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
Use versions to maintain model-specific prompts for the same instructions. For example:

```python
from prompt_versions_manager import PromptVersionsManager

p = PromptVersionsManager()

# First, set different prompt values for the same key for each model version
p.version("gpt4").set(
    "system.role",
    "You are GPT-4, a large language model trained by OpenAI. Follow the user's instructions carefully and format responses appropriately."
)

p.version("claude").set(
    "system.role",
    "You are Claude, an AI assistant created by Anthropic to be helpful, harmless, and honest. Always approach tasks thoughtfully and aim to provide accurate, nuanced responses."
)

p.version("llama2").set(
    "system.role",
    "You are Llama 2, an AI assistant trained by Meta. Provide direct, factual responses and always maintain a helpful and respectful tone."
)

# Attempting to overwrite without permission will raise an error
try:
    p.version("gpt4").set(
        "system.role",
        "A different system role"  # This will raise ValueError
    )
except ValueError as e:
    print(e)  # Prompt 'system.role' already exists in version 'gpt4'. Set overwrite=True to update it.

# To update an existing prompt, explicitly set overwrite=True
p.version("gpt4").set(
    "system.role",
    "You are GPT-4, an advanced AI model. You excel at complex reasoning and provide detailed, accurate responses.",
    overwrite=True  # Now it will update the existing prompt
)

# Now you can get model-specific responses using the same prompt key
gpt4_response = p.version("gpt4").t("system.role")
claude_response = p.version("claude").t("system.role")
llama_response = p.version("llama2").t("system.role")

# Get all versions of the same prompt key
versions = p.get_all_versions("system.role")
# Returns: [
#   {"version": "gpt4", "value": "You are GPT-4, an advanced AI model..."},
#   {"version": "claude", "value": "You are Claude, an AI assistant..."},
#   {"version": "llama2", "value": "You are Llama 2, an AI assistant..."}
# ]
```

### Multiple Prompt Sets
Use named managers to handle different types of prompts, each with their own versions:

```python
# Setup managers for different use cases
chat = PromptVersionsManager.setup("chat")
code = PromptVersionsManager.setup("code")

# Set different versions of the same chat prompt
chat.version("formal").set(
    "assist.task",
    "I understand you need assistance with {task}. Let me analyze your requirements: {requirements}"
)

chat.version("casual").set(
    "assist.task",
    "I'll help you with {task}! Looking at your requirements: {requirements}"
)

# Try to modify an existing prompt (will fail without overwrite=True)
try:
    chat.version("formal").set(
        "assist.task",
        "Let me help you with {task}. Your requirements are: {requirements}"
    )
except ValueError:
    print("Cannot overwrite existing prompt without overwrite=True")

# Set different versions of the same code review prompt
code.version("detailed").set(
    "review.code",
    "I'll perform a comprehensive review of your {language} code, analyzing: architecture, performance, security, and best practices."
)

code.version("quick").set(
    "review.code",
    "I'll do a quick review of your {language} code, focusing on critical issues and basic improvements."
)

# Use the same prompt keys with different versions
formal_response = chat.version("formal").t("assist.task", 
    task="data analysis", 
    requirements="must be scalable")

casual_response = chat.version("casual").t("assist.task",
    task="data analysis",
    requirements="must be scalable")

detailed_review = code.version("detailed").t("review.code", language="Python")
quick_review = code.version("quick").t("review.code", language="Python")
```

Your `prompts` directory could look like:
```
prompts/
├── chat/
│   ├── formal.json
│   └── casual.json
├── code/
│   ├── detailed.json
│   └── quick.json
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

# Set a prompt with placeholders
p.set(
    "introduce.expert",
    "I am a highly knowledgeable {field} expert with {years} years of experience. I can provide detailed, accurate information about {specialization}."
)

# Use the prompt with different parameters
ml_expert = p.t("introduce.expert",
                field="machine learning",
                years="10",
                specialization="neural networks")

# Set different versions of the same prompt
p.version("technical").set(
    "analyze.code",
    "Perform a technical analysis of this {language} code, focusing on {aspect}. Provide specific recommendations for improvement."
)

p.version("simple").set(
    "analyze.code",
    "Look at this {language} code and suggest simple ways to make it better, especially regarding {aspect}."
)

# Attempting to overwrite without permission will raise an error
try:
    p.version("technical").set(
        "analyze.code",
        "A different analysis prompt"  # This will raise ValueError
    )
except ValueError as e:
    print(e)  # Prompt 'analyze.code' already exists in version 'technical'. Set overwrite=True to update it.

# To update an existing prompt, explicitly set overwrite=True
p.version("technical").set(
    "analyze.code",
    "Perform a technical analysis of this {language} code, focusing on {aspect}. Provide specific recommendations for improvement.",
    overwrite=True  # Now it will update the existing prompt
)

# Use different versions of the same prompt
technical_review = p.version("technical").t("analyze.code",
                                          language="Python",
                                          aspect="performance")

simple_review = p.version("simple").t("analyze.code",
                                    language="Python",
                                    aspect="performance")

# List all versions
versions = p.versions()  # ['technical', 'simple']

# Find all versions of a specific prompt
analysis_versions = p.versions_for("analyze.code")
```

## FastAPI Integration 🌐

```python
from fastapi import FastAPI
from prompt_versions_manager import PromptVersionsManager

app = FastAPI()
chat = PromptVersionsManager("chat")
code = PromptVersionsManager("code")

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

Each named manager gets its own subdirectory with version-specific files:

```
prompts/
├── chat/                # Chat prompts
│   ├── formal.json
│   └── casual.json
├── code/               # Code assistance prompts
│   ├── detailed.json
│   └── quick.json
└── default/
    └── v1.json
```

Example `chat/formal.json`:
```json
{
  "assist.task": "I understand you need assistance with {task}. Let me analyze your requirements: {requirements}",
  "introduce.expert": "I am a highly knowledgeable {field} expert with {years} years of experience. I can provide detailed, accurate information about {specialization}."
}
```

## Contributing 🤝

We love contributions! Feel free to:

1. Fork the repository
2. Create a feature branch
3. Submit a pull request

## License 📄

MIT License - feel free to use this in your projects!
