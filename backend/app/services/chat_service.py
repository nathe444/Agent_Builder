from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.user import User
from app.models.message import MessageRole

from app.services.conversation_service import (
    conversation_service
)
from app.services.message_service import (
    message_service
)

from app.vectorstore.search_service import (
    search_service
)

from app.prompts.context_formatter import (
    context_formatter
)

from app.prompts.chat_prompt import (
    chat_prompt_builder
)

from app.llms.llm_service import (
    llm_service
)

from typing import Iterator

class ChatService:

    @staticmethod
    def prepare_chat(
        conversation_id: int,
        question: str,
        current_user: User,
        db: Session,
    ):
        # --------------------------------------------------
        # 1. Validate conversation ownership
        # --------------------------------------------------

        conversation = (
            conversation_service.get_conversation(
                conversation_id=conversation_id,
                current_user=current_user,
                db=db,
            )
        )

        # --------------------------------------------------
        # 2. Validate question
        # --------------------------------------------------

        question = question.strip()

        if not question:
            raise HTTPException(
                status_code=400,
                detail="Question cannot be empty"
            )

        # --------------------------------------------------
        # 3. Save user's message
        # --------------------------------------------------

        message_service.create_message(
            conversation=conversation,
            role=MessageRole.USER,
            content=question,
            db=db,
        )

        # --------------------------------------------------
        # 4. Get previous conversation history
        # --------------------------------------------------

        messages = message_service.get_messages(
            conversation=conversation,
            db=db,
        )

        # Remove the current question because we're going
        # to provide it separately to the prompt builder.
        history = []

        for message in messages[:-1]:

            history.append(
                {
                    "role": message.role.value,
                    "content": message.content,
                }
            )

        # --------------------------------------------------
        # 5. Retrieve relevant chunks
        # --------------------------------------------------

        chunks = search_service.search(
            chatbot_id=conversation.chatbot_id,
            query=question,
            db=db,
            retrieval_limit=20,
            rerank_limit=5,
        )

        # --------------------------------------------------
        # 6. Format retrieved context
        # --------------------------------------------------

        context = context_formatter.format(
            chunks
        )

        # --------------------------------------------------
        # 7. Build LLM messages
        # --------------------------------------------------

        prompt_messages = (
            chat_prompt_builder.build_messages(
                question=question,
                context=context,
                history=history,
            )
        )

        return conversation, prompt_messages, chunks

    @staticmethod
    def chat(
        conversation_id: int,
        question: str,
        current_user: User,
        db: Session,
    ):

        (
            conversation,
            prompt_messages,
            chunks,
        ) = ChatService.prepare_chat(
            conversation_id=conversation_id,
            question=question,
            current_user=current_user,
            db=db,
        )

        # --------------------------------------------------
        # Call LLM
        # --------------------------------------------------

        answer = llm_service.chat(
            messages=prompt_messages
        )

        # --------------------------------------------------
        # Prepare citations
        # --------------------------------------------------

        citations = []

        for chunk in chunks:

            citations.append(
                {
                    "document_id": chunk.get(
                        "document_id"
                    ),
                    "chunk_id": chunk.get(
                        "id"
                    ),
                    "score": chunk.get(
                        "relevance_score"
                    ),
                }
            )

        # --------------------------------------------------
        # Save assistant message
        # --------------------------------------------------

        assistant_message = (
            message_service.create_message(
                conversation=conversation,
                role=MessageRole.ASSISTANT,
                content=answer,
                citations=citations,
                db=db,
            )
        )

        # --------------------------------------------------
        # Return result
        # --------------------------------------------------

        return {
            "conversation_id": conversation.id,
            "message_id": assistant_message.id,
            "answer": answer,
            "citations": citations,
        }

    @staticmethod
    def chat_stream(
        conversation_id: int,
        question: str,
        current_user: User,
        db: Session,
    ) -> Iterator[str]:

        (
            conversation,
            prompt_messages,
            chunks,
        ) = ChatService.prepare_chat(
            conversation_id=conversation_id,
            question=question,
            current_user=current_user,
            db=db,
        )

        full_answer = ""

        try:

            stream = llm_service.chat_stream(
                messages=prompt_messages
            )

            for token in stream:

                full_answer += token

                yield token

            # Save completed assistant response
            citations = []

            for chunk in chunks:

                citations.append(
                    {
                        "document_id": chunk.get(
                            "document_id"
                        ),
                        "chunk_id": chunk.get(
                            "id"
                        ),
                        "score": chunk.get(
                            "relevance_score"
                        ),
                    }
                )

            message_service.create_message(
                conversation=conversation,
                role=MessageRole.ASSISTANT,
                content=full_answer,
                citations=citations,
                db=db,
            )

        except Exception:

            db.rollback()

            raise


chat_service = ChatService()