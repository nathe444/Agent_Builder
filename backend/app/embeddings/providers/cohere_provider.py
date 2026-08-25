import os
import cohere

from app.embeddings.providers.base import BaseEmbeddingProvider


class CohereProvider(BaseEmbeddingProvider):

    def __init__(self):

        self.client = cohere.ClientV2(
            api_key=os.getenv("COHERE_API_KEY")
        )

        self.model = os.getenv(
            "EMBEDDING_MODEL",
            "embed-v4.0"
        )

    def embed_documents(self, texts):

        response = self.client.embed(
            model=self.model,
            texts=texts,
            input_type="search_document"
        )

        return response.embeddings.float

    def embed_query(self, text):

        response = self.client.embed(
            model=self.model,
            texts=[text],
            input_type="search_query"
        )

        return response.embeddings.float[0]