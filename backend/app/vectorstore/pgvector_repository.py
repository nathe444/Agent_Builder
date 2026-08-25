from sqlalchemy import text
from sqlalchemy.orm import Session


class PgVectorRepository:

    @staticmethod
    def similarity_search(
        chatbot_id: int,
        embedding: list[float],
        db: Session,
        limit: int = 20
    ):

        sql = text("""
            SELECT
                id,
                document_id,
                content,
                chunk_metadata,
                embedding <=> CAST(:embedding AS vector) AS distance

            FROM document_chunks

            WHERE chatbot_id = :chatbot_id
            AND embedding IS NOT NULL

            ORDER BY embedding <=> CAST(:embedding AS vector)

            LIMIT :limit
        """)

        return db.execute(
            sql,
            {
                "embedding": embedding,
                "chatbot_id": chatbot_id,
                "limit": limit
            }
        ).mappings().all()


pgvector_repository = PgVectorRepository()