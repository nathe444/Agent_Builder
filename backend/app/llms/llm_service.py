from app.llms.provider_factory import (
    LLMProviderFactory
)


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


llm_service = LLMService()