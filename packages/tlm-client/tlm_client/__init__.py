"""tlm-client: Unified Ollama client for AI Test Toolkit."""

from .client import TLMClient
from .config import TLMConfig
from .exceptions import TLMError, TLMConnectionError, TLMTimeoutError, TLMModelError

__all__ = [
    "TLMClient",
    "TLMConfig",
    "TLMError",
    "TLMConnectionError",
    "TLMTimeoutError",
    "TLMModelError",
]
__version__ = "0.1.0"
