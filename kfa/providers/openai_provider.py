import os
from typing import List, Dict
from .base import BaseProvider

# OpenAI Python SDK v1.x
from openai import OpenAI

class OpenAIProvider(BaseProvider):
    def __init__(self):
        # API key is read from env via the SDK
        self.client = OpenAI()

    def respond(self, messages: List[Dict[str, str]], model: str, **kwargs) -> str:
        # Use Responses API for consistency
        resp = self.client.responses.create(
            model=model,
            input=[{"role": m["role"], "content": m["content"]} for m in messages],
            temperature=kwargs.get("temperature", 0.2),
            max_output_tokens=kwargs.get("max_output_tokens", 1500),
        )
        return resp.output_text
