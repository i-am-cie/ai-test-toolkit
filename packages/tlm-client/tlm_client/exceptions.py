"""Exceptions for TLM Client."""

class TLMError(Exception):
    """Base exception for TLM errors."""
    pass


class TLMConnectionError(TLMError):
    """Raised when connection to Ollama fails."""
    pass


class TLMTimeoutError(TLMError):
    """Raised when request to Ollama times out."""
    pass


class TLMModelError(TLMError):
    """Raised when model-related error occurs (not found, load failed, etc.)."""
    pass


class TLMValidationError(TLMError):
    """Raised when response validation fails."""
    pass
