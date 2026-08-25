import os

from app.embeddings.providers.cohere_provider import CohereProvider


class EmbeddingProviderFactory:

    @staticmethod
    def get_provider():

        provider = os.getenv(
            "EMBEDDING_PROVIDER",
            "cohere"
        )

        match provider:

            case "cohere":
                return CohereProvider()

            case _:
                raise ValueError(
                    f"Unknown provider: {provider}"
                )