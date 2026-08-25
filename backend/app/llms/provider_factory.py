import os

from app.llms.providers.cohere_provider import (
    CohereProvider
)


class LLMProviderFactory:

    @staticmethod
    def get_provider():

        provider = os.getenv(
            "LLM_PROVIDER",
            "cohere"
        )

        if provider == "cohere":
            return CohereProvider()

        raise ValueError(
            f"Unsupported provider: {provider}"
        )