"""
Ollama Helper for MarkItDown
Created by Captain CP

Makes it easy to use local Ollama models with MarkItDown
without needing to configure OpenAI client manually.
"""

from typing import Optional
import os


def get_ollama_client(
    base_url: str = "http://localhost:11434/v1",
    api_key: str = "ollama"
):
    """
    Get an OpenAI-compatible client configured for Ollama.
    
    Args:
        base_url: Ollama API endpoint (default: http://localhost:11434/v1)
        api_key: API key (Ollama doesn't need a real one, default: "ollama")
    
    Returns:
        OpenAI client configured for Ollama
    
    Example:
        >>> from markitdown import MarkItDown
        >>> from markitdown.ollama_helper import get_ollama_client
        >>> 
        >>> client = get_ollama_client()
        >>> md = MarkItDown(llm_client=client, llm_model="llama3.2-vision")
        >>> result = md.convert("image.jpg")
    """
    try:
        from openai import OpenAI
    except ImportError:
        raise ImportError(
            "OpenAI library required for Ollama integration. "
            "Install with: pip install openai"
        )
    
    return OpenAI(base_url=base_url, api_key=api_key)


def auto_detect_ollama(prefer_vision: bool = True) -> Optional[str]:
    """
    Auto-detect available Ollama models.
    
    Args:
        prefer_vision: If True, prefer vision-capable models
    
    Returns:
        Model name if found, None otherwise
    """
    try:
        import subprocess
        
        result = subprocess.run(
            ["ollama", "list"],
            capture_output=True,
            text=True,
            timeout=5
        )
        
        if result.returncode != 0:
            return None
        
        # Parse the text output (not JSON)
        lines = result.stdout.strip().split('\n')
        if len(lines) < 2:  # Need at least header + one model
            return None
        
        models = []
        for line in lines[1:]:  # Skip header
            if line.strip():
                model_name = line.split()[0]  # First column is model name
                models.append(model_name)
        
        if not models:
            return None
        
        # Prefer vision models if requested
        if prefer_vision:
            vision_models = [
                m for m in models 
                if "vision" in m.lower() or "llava" in m.lower()
            ]
            if vision_models:
                return vision_models[0]
        
        # Return first available model
        return models[0]
        
    except Exception:
        return None


class OllamaMarkItDown:
    """
    Convenience wrapper for MarkItDown with Ollama.
    
    Example:
        >>> from markitdown.ollama_helper import OllamaMarkItDown
        >>> 
        >>> md = OllamaMarkItDown(model="llama3.2-vision")
        >>> result = md.convert("document.pdf")
        >>> print(result.text_content)
    """
    
    def __init__(
        self,
        model: Optional[str] = None,
        base_url: str = "http://localhost:11434/v1",
        auto_detect: bool = True
    ):
        """
        Initialize MarkItDown with Ollama.
        
        Args:
            model: Ollama model name (e.g., "llama3.2-vision")
            base_url: Ollama API endpoint
            auto_detect: If True and model is None, auto-detect available models
        """
        from markitdown import MarkItDown
        
        if model is None and auto_detect:
            model = auto_detect_ollama()
            if model is None:
                raise RuntimeError(
                    "No Ollama models found. Install with: ollama pull llama3.2-vision"
                )
        
        self.model = model
        self.client = get_ollama_client(base_url=base_url)
        
        # Initialize MarkItDown with Ollama client if we have a model
        if self.model:
            self.md = MarkItDown(llm_client=self.client, llm_model=self.model)
        else:
            self.md = MarkItDown()
    
    def convert(self, *args, **kwargs):
        """Convert a file using MarkItDown with Ollama."""
        return self.md.convert(*args, **kwargs)
