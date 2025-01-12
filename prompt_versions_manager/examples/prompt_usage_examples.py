from prompt_versions_manager import PromptVersionsManager

def basic_usage_example():
    """Basic example of using prompts with the simplified API"""
    # Initialize the prompt manager (uses default settings)
    prompts = PromptVersionsManager()
    
    # Basic usage with default version (v1)
    system_prompt = prompts.t("system_prompt")
    print("Default System Prompt:", system_prompt)
    
    # Using a prompt with placeholders
    welcome = prompts.t("welcome.message.{name}", name="John")
    print("\nWelcome message:", welcome)
    # The key in the JSON will be "welcome.message" and value will be "welcome.message.{name}"
    
    # Reuse the same prompt with different variables
    welcome_alice = prompts.t("welcome.message", name="Alice")
    print("Welcome message for Alice:", welcome_alice)
    
    # Switch version and use complex prompt
    complex_prompt = (prompts.version("v2")
                      .t("debug.code.{language}.{aspect}",
                         language="Python",
                         aspect="performance"))
    print("\nComplex prompt:", complex_prompt)
    # The key in v2.json will be "debug.code" with placeholders in value

def named_managers_example():
    """Example of using multiple prompt managers for different use cases"""
    # Setup managers for different use cases
    chat = PromptVersionsManager.setup("chat")
    email = PromptVersionsManager.setup("email")
    
    # Chat prompts
    chat.set("greeting", "Hey {name}! How can I help you today?")
    chat.set("farewell", "Thanks for chatting, {name}! Have a great day!")
    
    # Email prompts
    email.set("subject.welcome", "Welcome to our service, {name}!")
    email.set("body.welcome", """
Dear {name},

Thank you for joining our service! We're excited to have you on board.

Best regards,
The Team
""")
    
    # Use chat prompts
    print("=== Chat Prompts ===")
    print(chat.t("greeting", name="Alice"))
    print(chat.t("farewell", name="Alice"))
    
    # Use email prompts
    print("\n=== Email Prompts ===")
    print(email.t("subject.welcome", name="Bob"))
    print(email.t("body.welcome", name="Bob"))
    
    # Show available versions for each manager
    print("\n=== Available Versions ===")
    print("Chat versions:", chat.versions())
    print("Email versions:", email.versions())

def versioning_example():
    """Example of working with different prompt versions"""
    # Setup with custom prompts directory
    p = PromptVersionsManager.setup("dev", 
        prompts_dir="./dev_prompts",
        default_version="dev"
    )
    
    # Create different versions of a prompt
    p.version("v1").set("intro.{role}", "You are a {role}")
    p.version("v2").set("intro.{role}", "You are now acting as a {role}")
    p.version("v3").set("intro.{role}", "I want you to take on the role of a {role}")
    
    # Get all versions with placeholders filled in
    versions = p.get_all_versions("intro.{role}", role="helpful assistant")
    print("=== All Versions of Intro Prompt ===")
    for v in versions:
        print(f"{v['version']}: {v['value']}")
    
    # Create prompts with different placeholders
    p.version("v1").set("task.{language}", "Write code in {language}")
    p.version("v2").set("task.{language}.{task}", "Write {language} code to {task}")
    
    # Get versions that match the given placeholders
    versions = p.get_all_versions("task.{language}", language="Python")
    print("\n=== Matching Versions of Task Prompt ===")
    for v in versions:
        print(f"{v['version']}: {v['value']}")
    
    # The v2 version won't be included since it requires an additional 'task' parameter
    
    # Get versions with all required placeholders
    versions = p.get_all_versions("task.{language}.{task}", 
                                language="Python",
                                task="sort a list")
    print("\n=== All Task Versions with Full Context ===")
    for v in versions:
        print(f"{v['version']}: {v['value']}")

def fastapi_integration_example():
    """Example of using prompt manager in a FastAPI application"""
    from fastapi import FastAPI, HTTPException
    
    app = FastAPI()
    chat = PromptVersionsManager("chat")
    email = PromptVersionsManager("email")
    
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
