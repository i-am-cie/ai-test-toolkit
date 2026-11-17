"""Configuration for TLM Client."""

from pydantic import BaseModel, Field
from typing import Optional


class TLMConfig(BaseModel):
    """Configuration for Ollama connection and model parameters."""
    
    # Connection
    host: str = Field(default="http://localhost:11434", description="Ollama host URL")
    timeout: float = Field(default=120.0, description="Request timeout in seconds")
    
    # Model
    model: str = Field(default="qwen2.5:7b", description="Model name to use")
    temperature: float = Field(default=0.3, description="Sampling temperature")
    top_p: float = Field(default=0.9, description="Top-p sampling")
    num_predict: int = Field(default=4096, description="Max tokens to generate")
    
    # Retry
    max_retries: int = Field(default=3, description="Max retry attempts")
    retry_delay: float = Field(default=1.0, description="Base delay between retries")
    
    # Context
    num_ctx: int = Field(default=8192, description="Context window size")
    
    def to_ollama_options(self) -> dict:
        """Convert to Ollama options dict."""
        return {
            "temperature": self.temperature,
            "top_p": self.top_p,
            "num_predict": self.num_predict,
            "num_ctx": self.num_ctx,
        }


# Default config instance
DEFAULT_CONFIG = TLMConfig()
