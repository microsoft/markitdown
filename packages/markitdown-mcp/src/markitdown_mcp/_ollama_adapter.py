"""
Ollama native API adapter.

Provides an OpenAI-client-compatible wrapper around Ollama's native
/api/generate and /api/chat endpoints.  This is used as a fallback when
Ollama's built-in /v1/chat/completions endpoint is unavailable or
returns errors (e.g. 502 on certain Ollama versions).

LM Studio, vLLM, and other OpenAI-compatible servers do NOT need this
adapter — they work directly with the standard ``openai.OpenAI`` client.
"""

import json
import urllib.request
from typing import Any


class OllamaChatCompletion:
    """Minimal stand-in for ``openai.types.chat.ChatCompletion``."""

    def __init__(self, content: str) -> None:
        self.choices = [self._Choice(content)]

    class _Choice:
        def __init__(self, content: str) -> None:
            self.message = self._Message(content)

        class _Message:
            def __init__(self, content: str) -> None:
                self.content = content


class OllamaCompletions:
    """Minimal stand-in for ``openai.resources.chat.Completions``."""

    def __init__(self, base_url: str, model: str) -> None:
        self._base_url = base_url.rstrip("/")
        self._model = model

    def create(
        self,
        *,
        model: str | None = None,
        messages: list[dict[str, Any]],
        **kwargs: Any,
    ) -> OllamaChatCompletion:
        """Send a chat-completion request to Ollama's native API.

        Routes vision requests (messages containing ``image_url`` parts)
        to ``/api/generate`` and text-only requests to ``/api/chat``.
        """
        actual_model = model or self._model

        # Unpack OpenAI-format messages into prompt text + images
        images: list[str] = []
        prompt_text = ""

        for msg in messages:
            content = msg.get("content", "")
            if isinstance(content, list):
                for part in content:
                    if part.get("type") == "text":
                        prompt_text += part.get("text", "")
                    elif part.get("type") == "image_url":
                        data_uri = part.get("image_url", {}).get("url", "")
                        if "," in data_uri:
                            images.append(data_uri.split(",", 1)[1])
                        else:
                            images.append(data_uri)
            else:
                prompt_text += str(content)

        if images:
            payload: dict[str, Any] = {
                "model": actual_model,
                "prompt": prompt_text,
                "images": images,
                "stream": False,
            }
            endpoint = f"{self._base_url}/api/generate"
        else:
            payload = {
                "model": actual_model,
                "messages": [{"role": "user", "content": prompt_text}],
                "stream": False,
            }
            endpoint = f"{self._base_url}/api/chat"

        req = urllib.request.Request(
            endpoint,
            data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json"},
        )

        try:
            with urllib.request.urlopen(req, timeout=300) as resp:
                result = json.loads(resp.read())
        except Exception as exc:
            raise RuntimeError(
                f"Ollama API call to {endpoint} failed: {exc}"
            ) from exc

        # /api/generate returns "response"; /api/chat returns "message"
        content: str = result.get("response") or result.get(
            "message", {}
        ).get("content", "")
        return OllamaChatCompletion(content)


class OllamaClient:
    """Minimal stand-in for ``openai.OpenAI``.

    Can be passed directly as ``llm_client`` to ``MarkItDown``.
    """

    def __init__(
        self,
        base_url: str = "http://localhost:11434",
        model: str = "",
    ) -> None:
        self.chat = type(
            "_Chat",
            (),
            {"completions": OllamaCompletions(base_url, model)},
        )()
