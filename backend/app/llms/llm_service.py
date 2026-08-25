from app.llms.provider_factory import (
    LLMProviderFactory
)

from typing import Iterator


class LLMService:

    def __init__(self):

        self.provider = (
            LLMProviderFactory
            .get_provider()
        )

    def chat(
        self,
        messages: list[dict]
    ) -> str:

        return self.provider.chat(
            messages
        )

    
    def chat_stream(
        self,
        messages: list[dict]
    ) -> Iterator[str]:

        return self.provider.chat_stream(
            messages
        )


llm_service = LLMService()