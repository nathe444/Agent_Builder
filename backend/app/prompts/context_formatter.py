class ContextFormatter:

    @staticmethod
    def format(chunks: list[dict]) -> str:

        if not chunks:
            return "No relevant context was found."

        formatted = []

        for index, chunk in enumerate(chunks, start=1):

            content = chunk.get(
                "content",
                ""
            )

            metadata = chunk.get(
                "metadata",
                {}
            )

            document_id = chunk.get(
                "document_id"
            )

            formatted.append(
                f"""
[Source {index}]
Document ID: {document_id}
Metadata: {metadata}

{content}
""".strip()
            )

        return "\n\n---\n\n".join(
            formatted
        )


context_formatter = ContextFormatter()