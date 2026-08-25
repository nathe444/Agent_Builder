from typing import Optional


DEFAULT_SYSTEM_PROMPT = """
You are a helpful AI assistant.

Answer the user's question using the provided context.

Rules:
1. Use the provided context as the primary source of truth.
2. If the context does not contain enough information to answer the question, say that you do not have enough information.
3. Do not invent facts.
4. Be concise and clear.
5. When possible, cite the relevant sources from the provided context.
"""


class ChatPromptBuilder:

    @staticmethod
    def build_messages(
        question: str,
        context: str,
        history: Optional[list[dict]] = None,
        system_prompt: Optional[str] = None,
    ) -> list[dict]:

        system_content = (
            system_prompt.strip()
            if system_prompt
            else DEFAULT_SYSTEM_PROMPT.strip()
        )

        messages = [
            {
                "role": "system",
                "content": system_content,
            }
        ]

        # Add previous conversation messages
        if history:
            messages.extend(history)

        # Add retrieved context + current question
        user_content = f"""
Context:

{context}

---

User Question:

{question}
""".strip()

        messages.append(
            {
                "role": "user",
                "content": user_content,
            }
        )

        return messages


chat_prompt_builder = ChatPromptBuilder()