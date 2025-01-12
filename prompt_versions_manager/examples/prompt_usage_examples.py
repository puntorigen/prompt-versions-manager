from prompt_versions_manager import PromptVersionsManager

def basic_usage_example():
    """Basic example of using prompts with the simplified API"""
    # Initialize the prompt manager (uses default settings)
    prompts = PromptVersionsManager()
    
    # Basic usage with default version (v1)
    prompts.set("system.role", 
        "You are a helpful AI assistant. Always provide clear and concise responses.")
    print("Default System Role:", prompts.t("system.role"))
    
    # Try to modify the prompt (will raise error)
    try:
        prompts.set("system.role", "A different system role")
        print("This line won't be reached")
    except ValueError as e:
        print("\nOverwrite protection:", str(e))
    
    # Properly update an existing prompt
    prompts.set("system.role", 
        "You are an AI assistant focused on clarity and precision. Provide step-by-step explanations when helpful.",
        overwrite=True)
    print("\nUpdated System Role:", prompts.t("system.role"))
    
    # Using prompts with placeholders
    prompts.set("expert.role", 
        "You are an expert in {field} with {years} years of experience. Focus on {specialization}.")
    
    expert_prompt = prompts.t("expert.role",
                            field="machine learning",
                            years="10",
                            specialization="neural networks")
    print("\nExpert Role:", expert_prompt)

def named_managers_example():
    """Example of using multiple prompt managers for different use cases"""
    # Setup managers for different use cases
    chat = PromptVersionsManager.setup("chat")
    code = PromptVersionsManager.setup("code")
    
    # Chat prompts with different formality levels
    chat.version("formal").set("assist.task", 
        "I understand you need assistance with {task}. Let me analyze your requirements: {requirements}")
    
    chat.version("casual").set("assist.task",
        "I'll help you with {task}! Looking at your requirements: {requirements}")
    
    # Code review prompts with different detail levels
    code.version("detailed").set("review.code",
        """Perform a comprehensive review of this {language} code, analyzing:
        1. Architecture and design patterns
        2. Performance optimizations
        3. Security considerations
        4. Best practices and conventions
        5. Error handling and edge cases""")
    
    code.version("quick").set("review.code",
        "I'll do a quick review of your {language} code, focusing on critical issues and basic improvements.")
    
    # Use chat prompts with different formality
    print("=== Chat Prompts ===")
    print("Formal:", chat.version("formal").t("assist.task",
        task="data analysis",
        requirements="must be scalable and maintainable"))
    
    print("\nCasual:", chat.version("casual").t("assist.task",
        task="data analysis",
        requirements="must be scalable and maintainable"))
    
    # Use code review prompts with different detail levels
    print("\n=== Code Review Prompts ===")
    print("Detailed:", code.version("detailed").t("review.code", language="Python"))
    print("\nQuick:", code.version("quick").t("review.code", language="Python"))

def versioning_example():
    """Example of working with different prompt versions for different LLM models"""
    # Setup with custom prompts directory
    p = PromptVersionsManager.setup("models", 
        prompts_dir="./model_prompts",
        default_version="gpt4"
    )
    
    # Set system prompts for different models
    p.version("gpt4").set("system.role",
        "You are GPT-4, a large language model trained by OpenAI. Follow instructions carefully and format responses appropriately.")
    
    p.version("claude").set("system.role",
        "You are Claude, an AI assistant created by Anthropic to be helpful, harmless, and honest.")
    
    p.version("llama2").set("system.role",
        "You are Llama 2, an AI assistant trained by Meta. Provide direct, factual responses while maintaining a helpful tone.")
    
    # Try to modify GPT-4's system role (will fail)
    try:
        p.version("gpt4").set("system.role", "A different system role")
    except ValueError as e:
        print("=== Overwrite Protection ===")
        print(str(e))
    
    # Properly update GPT-4's system role
    p.version("gpt4").set("system.role",
        "You are GPT-4, an advanced AI model. Excel at complex reasoning and provide detailed, accurate responses.",
        overwrite=True)
    
    # Get all versions of the system role
    versions = p.get_all_versions("system.role")
    print("\n=== System Roles Across Models ===")
    for v in versions:
        print(f"\n{v['version']}:", v['value'])

def fastapi_integration_example():
    """Example of using prompt manager in a FastAPI application"""
    from fastapi import FastAPI, HTTPException
    
    app = FastAPI()
    chat = PromptVersionsManager("chat")
    code = PromptVersionsManager("code")
    
    @app.get("/prompts/{manager}/{version}/{prompt_id}")
    async def get_prompt(manager: str, version: str, prompt_id: str, **params):
        try:
            p = PromptVersionsManager(manager)
            return {"prompt": p.version(version).t(prompt_id, **params)}
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))
    
    @app.get("/versions/{manager}")
    async def list_versions(manager: str):
        return {"versions": PromptVersionsManager(manager).versions()}
    
    @app.get("/versions/{manager}/{prompt_id}")
    async def get_prompt_versions(manager: str, prompt_id: str):
        return {"versions": PromptVersionsManager(manager).versions_for(prompt_id)}
    
    return app

if __name__ == "__main__":
    print("=== Basic Usage Example ===")
    basic_usage_example()
    
    print("\n=== Named Managers Example ===")
    named_managers_example()
    
    print("\n=== Versioning Example ===")
    versioning_example()
    
    print("\n=== FastAPI Integration Created ===")
    print("Run with: uvicorn examples.prompt_usage_examples:fastapi_integration_example()")
