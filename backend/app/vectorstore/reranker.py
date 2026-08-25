import os
import cohere


class CohereReranker:

    def __init__(self):

        self.client = cohere.ClientV2(
            api_key=os.getenv("COHERE_API_KEY")
        )

        self.model = os.getenv(
            "RERANK_MODEL",
            "rerank-v3.5"
        )

    def rerank(
        self,
        query: str,
        documents: list,
        top_n: int = 5
    ):

        if not documents:
            return []

        response = self.client.rerank(
            model=self.model,
            query=query,
            documents=[
                doc["content"]
                for doc in documents
            ],
            top_n=top_n
        )

        reranked = []

        for result in response.results:

            document = dict(documents[result.index])

            document["relevance_score"] = (
                result.relevance_score
            )

            reranked.append(document)

        return reranked


reranker = CohereReranker()