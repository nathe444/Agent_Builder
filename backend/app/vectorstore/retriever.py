from sqlalchemy.orm import Session

from app.embeddings.embedding_service import (
    embedding_service
)

from app.vectorstore.pgvector_repository import (
    pgvector_repository
)


class Retriever:

    @staticmethod
    def retrieve(
        chatbot_id: int,
        query: str,
        db: Session,
        limit: int = 20
    ):

        query_embedding = (
            embedding_service.embed_query(query)
        )

        return (
            pgvector_repository.similarity_search(
                chatbot_id=chatbot_id,
                embedding=query_embedding,
                db=db,
                limit=limit
            )
        )


retriever = Retriever()