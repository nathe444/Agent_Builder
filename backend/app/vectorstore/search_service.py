from sqlalchemy.orm import Session

from app.vectorstore.retriever import retriever
from app.vectorstore.reranker import reranker


class SearchService:

    @staticmethod
    def search(
        chatbot_id: int,
        query: str,
        db: Session,
        retrieval_limit: int = 20,
        rerank_limit: int = 5,
    ):

        # Step 1: Semantic Search
        retrieved_chunks = retriever.retrieve(
            chatbot_id=chatbot_id,
            query=query,
            db=db,
            limit=retrieval_limit,
        )

        # Step 2: Rerank
        reranked_chunks = reranker.rerank(
            query=query,
            documents=retrieved_chunks,
            top_n=rerank_limit,
        )

        return reranked_chunks


search_service = SearchService()