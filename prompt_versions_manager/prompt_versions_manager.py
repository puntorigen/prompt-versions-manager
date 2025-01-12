import json
from typing import Dict, Any, Optional
from pathlib import Path
import os
import re


class PromptVersionsManager:
    _instances: Dict[str, 'PromptVersionsManager'] = {}
    _placeholder_pattern = re.compile(r'{([^}]+)}')

    def __new__(cls, name: str = "default"):
        if name not in cls._instances:
            cls._instances[name] = super().__new__(cls)
            cls._instances[name]._initialized = False
            cls._instances[name]._name = name
        return cls._instances[name]

    def __init__(self, name: str = "default"):
        if self._initialized:
            return
            
        base_dir = os.getenv('PROMPTS_DIR', Path.cwd() / 'prompts')
        self._prompts_dir = Path(base_dir) / self._name
        self._current_version = os.getenv('PROMPT_VERSION', 'v1')
        self._dev_mode = os.getenv('PROMPT_DEV_MODE', 'true').lower() == 'true'  # Default to True
        self._prompt_cache: Dict[str, Dict[str, str]] = {}
        self._prompts_dir.mkdir(parents=True, exist_ok=True)
        self._load_prompts()
        self._initialized = True

    def _load_prompts(self):
        """Load all prompt files from the prompts directory"""
        if not self._prompts_dir.exists():
            return

        for file in self._prompts_dir.glob('*.json'):
            version = file.stem
            with open(file, 'r') as f:
                self._prompt_cache[version] = json.load(f)
            
        # Ensure current version exists
        if self._current_version not in self._prompt_cache:
            self._prompt_cache[self._current_version] = {}
            self._save_version(self._current_version)

    def _save_version(self, version: str):
        """Save prompts for a specific version to file"""
        file_path = self._prompts_dir / f"{version}.json"
        with open(file_path, 'w') as f:
            json.dump(self._prompt_cache[version], f, indent=2)

    def _clean_key(self, key: str) -> str:
        """Remove placeholder variables from key"""
        # Find the base key by taking everything before the first placeholder
        parts = key.split('{')
        base_key = parts[0].rstrip('.')
        return base_key

    def version(self, version: str) -> 'PromptVersionsManager':
        """Set the current prompt version"""
        self._current_version = version
        if version not in self._prompt_cache:
            self._prompt_cache[version] = {}
            self._save_version(version)
        return self

    def t(self, prompt_id: str, **kwargs) -> str:
        """
        Get a prompt by its ID, with optional formatting.
        Creates new prompts automatically using the prompt_id as the value.
        Handles placeholder variables in both keys and values.
        """
        if self._current_version not in self._prompt_cache:
            self._prompt_cache[self._current_version] = {}
        
        # Clean the key by removing any placeholder variables
        clean_key = self._clean_key(prompt_id)
        
        if clean_key not in self._prompt_cache[self._current_version]:
            # Store the original prompt_id as value
            self._prompt_cache[self._current_version][clean_key] = prompt_id
            self._save_version(self._current_version)
        
        # Get the template (either existing or newly created)
        prompt_template = self._prompt_cache[self._current_version][clean_key]
        
        # If kwargs are provided, format the template
        if kwargs:
            try:
                return prompt_template.format(**kwargs)
            except KeyError as e:
                raise ValueError(f"Missing formatting argument: {e}")
        
        return prompt_template

    def set(self, prompt_id: str, value: str) -> 'PromptVersionsManager':
        """
        Set or update a prompt value for the current version.
        The prompt_id can include placeholders - they will be stripped automatically.
        The value can include placeholders for later formatting with t().
        
        Example:
            p.set("greeting.{name}", "Hello {name}!")
            p.t("greeting", name="Alice")  # Returns: "Hello Alice!"
        
        Returns self for method chaining.
        """
        if self._current_version not in self._prompt_cache:
            self._prompt_cache[self._current_version] = {}
            
        clean_key = self._clean_key(prompt_id)
        self._prompt_cache[self._current_version][clean_key] = value
        self._save_version(self._current_version)
        return self

    @property
    def v(self) -> str:
        """Get current version"""
        return self._current_version

    def versions(self) -> list[str]:
        """Get a list of all available versions"""
        return sorted(self._prompt_cache.keys())

    def versions_for(self, prompt_id: str) -> dict[str, str]:
        """
        Get all available versions of a specific prompt.
        Returns a dictionary mapping version to prompt value.
        The prompt_id can include placeholders - they will be stripped automatically.
        """
        clean_key = self._clean_key(prompt_id)
        versions = {}
        
        for version, prompts in self._prompt_cache.items():
            if clean_key in prompts:
                versions[version] = prompts[clean_key]
        
        return versions

    def get_all_versions(self, prompt_id: str, **kwargs) -> list[dict[str, str]]:
        """
        Get all versions of a prompt with placeholders filled in.
        Returns a list of dicts with 'version' and 'value' keys.
        The value will have all placeholders replaced with the provided kwargs.
        
        Example:
            p.set("greeting", "Hello {name}!")
            p.version("v2").set("greeting", "Hi there, {name}!")
            
            versions = p.get_all_versions("greeting", name="Alice")
            # Returns: [
            #   {"version": "v1", "value": "Hello Alice!"},
            #   {"version": "v2", "value": "Hi there, Alice!"}
            # ]
        """
        versions = []
        raw_versions = self.versions_for(prompt_id)
        
        for version, template in raw_versions.items():
            try:
                formatted_value = template.format(**kwargs) if kwargs else template
                versions.append({
                    "version": version,
                    "value": formatted_value
                })
            except KeyError as e:
                # Skip versions that don't match the provided kwargs
                continue
        
        return sorted(versions, key=lambda x: x["version"])

    @classmethod
    def setup(cls, name: str = "default", prompts_dir: Optional[str] = None, 
             default_version: Optional[str] = None) -> 'PromptVersionsManager':
        """
        Setup a named prompt manager instance with custom configuration.
        
        Args:
            name: Name of the prompt manager instance. Different names use different prompt directories.
            prompts_dir: Base directory for all prompt managers. Each named instance gets a subdirectory.
            default_version: Default version to use for this instance.
        
        Example:
            # Setup different managers for different use cases
            chat_prompts = PromptVersionsManager.setup("chat")
            email_prompts = PromptVersionsManager.setup("email")
            
            # Each gets its own directory:
            # prompts/chat/v1.json
            # prompts/email/v1.json
        """
        if prompts_dir:
            os.environ['PROMPTS_DIR'] = prompts_dir
        if default_version:
            os.environ['PROMPT_VERSION'] = default_version
        
        # Reset the instance to reload with new config
        if name in cls._instances:
            del cls._instances[name]
        
        return cls(name)
