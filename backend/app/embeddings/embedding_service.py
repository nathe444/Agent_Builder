from app.embeddings.provider_factory import (
    EmbeddingProviderFactory
)


class EmbeddingService:

    def __init__(self):

        self.provider = (
            EmbeddingProviderFactory
            .get_provider()
        )

    def embed_texts(self, texts: list[str]):

        return self.provider.embed_documents(
            texts
        )

    def embed_query(self, query: str):

        return self.provider.embed_query(
            query
        )


embedding_service = EmbeddingService()