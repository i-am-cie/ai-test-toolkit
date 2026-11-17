"""TLM Client: Unified Ollama client for AI Test Toolkit."""

import asyncio
import json
import logging
from typing import Any, Dict, List, Optional, Union

import ollama
from pydantic import BaseModel

from .config import TLMConfig, DEFAULT_CONFIG
from .exceptions import TLMError, TLMConnectionError, TLMTimeoutError, TLMModelError

logger = logging.getLogger(__name__)


class ChatMessage(BaseModel):
    """Chat message model."""
    role: str
    content: str


class ChatResponse(BaseModel):
    """Chat response model."""
    message: ChatMessage
    done: bool = True
    total_duration: Optional[int] = None
    load_duration: Optional[int] = None
    prompt_eval_count: Optional[int] = None
    eval_count: Optional[int] = None
    eval_duration: Optional[int] = None


class TLMClient:
    """Unified client for interacting with Ollama models."""
    
    def __init__(self, config: Optional[TLMConfig] = None):
        """Initialize the TLM client.
        
        Args:
            config: Optional TLMConfig instance. Uses DEFAULT_CONFIG if not provided.
        """
        self.config = config or DEFAULT_CONFIG
        self._client: Optional[ollama.Client] = None
        self._async_client: Optional[ollama.AsyncClient] = None
    
    @property
    def client(self) -> ollama.Client:
        """Get or create synchronous Ollama client."""
        if self._client is None:
            self._client = ollama.Client(
                host=self.config.host,
                timeout=self.config.timeout,
            )
        return self._client
    
    @property
    def async_client(self) -> ollama.AsyncClient:
        """Get or create asynchronous Ollama client."""
        if self._async_client is None:
            self._async_client = ollama.AsyncClient(
                host=self.config.host,
                timeout=self.config.timeout,
            )
        return self._async_client
    
    def _get_options(self, overrides: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Get Ollama options with optional overrides."""
        options = self.config.to_ollama_options()
        if overrides:
            options.update(overrides)
        return options
    
    def chat(
        self,
        messages: List[Dict[str, str]],
        model: Optional[str] = None,
        options: Optional[Dict[str, Any]] = None,
        stream: bool = False,
    ) -> Union[ChatResponse, str]:
        """Send a chat completion request.
        
        Args:
            messages: List of message dicts with 'role' and 'content'
            model: Model name (uses config default if not provided)
            options: Optional overrides for generation parameters
            stream: Whether to stream the response
            
        Returns:
            ChatResponse or streamed content string
            
        Raises:
            TLMConnectionError: If connection to Ollama fails
            TLMTimeoutError: If request times out
            TLMModelError: If model-related error occurs
        """
        model = model or self.config.model
        options = self._get_options(options)
        
        for attempt in range(self.config.max_retries):
            try:
                response = self.client.chat(
                    model=model,
                    messages=messages,
                    options=options,
                    stream=stream,
                )
                
                if stream:
                    return self._handle_stream(response)
                
                return ChatResponse(
                    message=ChatMessage(
                        role=response["message"]["role"],
                        content=response["message"]["content"],
                    ),
                    done=response.get("done", True),
                    total_duration=response.get("total_duration"),
                    load_duration=response.get("load_duration"),
                    prompt_eval_count=response.get("prompt_eval_count"),
                    eval_count=response.get("eval_count"),
                    eval_duration=response.get("eval_duration"),
                )
                
            except ollama.ResponseError as e:
                if "model" in str(e).lower() and "not found" in str(e).lower():
                    raise TLMModelError(f"Model '{model}' not found. Run: ollama pull {model}")
                if attempt == self.config.max_retries - 1:
                    raise TLMError(f"Ollama error: {e}")
            except TimeoutError as e:
                if attempt == self.config.max_retries - 1:
                    raise TLMTimeoutError(f"Request timed out after {self.config.timeout}s")
            except ConnectionError as e:
                if attempt == self.config.max_retries - 1:
                    raise TLMConnectionError(f"Cannot connect to Ollama at {self.config.host}")
            except Exception as e:
                if attempt == self.config.max_retries - 1:
                    raise TLMError(f"Unexpected error: {e}")
            
            # Retry delay
            import time
            time.sleep(self.config.retry_delay * (attempt + 1))
        
        raise TLMError("Max retries exceeded")
    
    def _handle_stream(self, stream) -> str:
        """Handle streaming response."""
        full_content = []
        for chunk in stream:
            if "message" in chunk and "content" in chunk["message"]:
                content = chunk["message"]["content"]
                full_content.append(content)
        return "".join(full_content)
    
    async def async_chat(
        self,
        messages: List[Dict[str, str]],
        model: Optional[str] = None,
        options: Optional[Dict[str, Any]] = None,
    ) -> ChatResponse:
        """Async version of chat."""
        model = model or self.config.model
        options = self._get_options(options)
        
        for attempt in range(self.config.max_retries):
            try:
                response = await self.async_client.chat(
                    model=model,
                    messages=messages,
                    options=options,
                )
                return ChatResponse(
                    message=ChatMessage(
                        role=response["message"]["role"],
                        content=response["message"]["content"],
                    ),
                    done=response.get("done", True),
                )
            except ollama.ResponseError as e:
                if "model" in str(e).lower() and "not found" in str(e).lower():
                    raise TLMModelError(f"Model '{model}' not found. Run: ollama pull {model}")
                if attempt == self.config.max_retries - 1:
                    raise TLMError(f"Ollama error: {e}")
            except TimeoutError as e:
                if attempt == self.config.max_retries - 1:
                    raise TLMTimeoutError(f"Request timed out after {self.config.timeout}s")
            except ConnectionError as e:
                if attempt == self.config.max_retries - 1:
                    raise TLMConnectionError(f"Cannot connect to Ollama at {self.config.host}")
            except Exception as e:
                if attempt == self.config.max_retries - 1:
                    raise TLMError(f"Unexpected error: {e}")
            
            await asyncio.sleep(self.config.retry_delay * (attempt + 1))
        
        raise TLMError("Max retries exceeded")
    
    def generate(
        self,
        prompt: str,
        model: Optional[str] = None,
        options: Optional[Dict[str, Any]] = None,
    ) -> str:
        """Generate text from a prompt (non-chat mode)."""
        model = model or self.config.model
        options = self._get_options(options)
        
        for attempt in range(self.config.max_retries):
            try:
                response = self.client.generate(
                    model=model,
                    prompt=prompt,
                    options=options,
                )
                return response.get("response", "")
            except ollama.ResponseError as e:
                if "model" in str(e).lower() and "not found" in str(e).lower():
                    raise TLMModelError(f"Model '{model}' not found. Run: ollama pull {model}")
                if attempt == self.config.max_retries - 1:
                    raise TLMError(f"Ollama error: {e}")
            except TimeoutError as e:
                if attempt == self.config.max_retries - 1:
                    raise TLMTimeoutError(f"Request timed out after {self.config.timeout}s")
            except ConnectionError as e:
                if attempt == self.config.max_retries - 1:
                    raise TLMConnectionError(f"Cannot connect to Ollama at {self.config.host}")
            except Exception as e:
                if attempt == self.config.max_retries - 1:
                    raise TLMError(f"Unexpected error: {e}")
            
            import time
            time.sleep(self.config.retry_delay * (attempt + 1))
        
        raise TLMError("Max retries exceeded")
    
    def check_model(self, model: Optional[str] = None) -> bool:
        """Check if model is available locally."""
        model = model or self.config.model
        try:
            models = self.client.list()
            return any(m.get("name", "").startswith(model.split(":")[0]) for m in models.get("models", []))
        except Exception:
            return False
    
    def pull_model(self, model: Optional[str] = None) -> bool:
        """Pull model from Ollama registry."""
        model = model or self.config.model
        try:
            self.client.pull(model)
            return True
        except Exception as e:
            logger.error(f"Failed to pull model {model}: {e}")
            return False
