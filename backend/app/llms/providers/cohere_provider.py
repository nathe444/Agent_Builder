import os
import cohere
from typing import Iterator

from app.llms.providers.base import BaseLLMProvider


class CohereProvider(BaseLLMProvider):

    def __init__(self):

        api_key = os.getenv("COHERE_API_KEY")

        if not api_key:
            raise ValueError(
                "COHERE_API_KEY is not configured"
            )

        self.client = cohere.ClientV2(
            api_key=api_key
        )

        self.model = os.getenv(
            "CHAT_MODEL",
            "command-a-03-2025"
        )

    def chat(
        self,
        messages: list[dict]
    ) -> str:

        response = self.client.chat(
            model=self.model,
            messages=messages,
        )

        if not response.message.content:
            return ""

        return response.message.content[0].text

    

    def chat_stream(
        self,
        messages: list[dict]
    ) -> Iterator[str]:

        response = self.client.chat_stream(
            model=self.model,
            messages=messages
        )

        for event in response:

            if event.type == "content-delta":

                if event.delta and event.delta.message:
                    content = event.delta.message.content
                    if isinstance(content, str):
                        yield content
                    elif hasattr(content, 'text'):
                        yield content.text
                    elif isinstance(content, list) and len(content) > 0:
                        yield content[0].text if hasattr(content[0], 'text') else str(content[0])