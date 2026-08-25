import json

from langchain_core.documents import Document

from app.ingestion.loaders.base import BaseLoader


class JSONLoader(BaseLoader):

    def __init__(self, path: str):
        self.path = path

    def load(self) -> list[Document]:
        with open(self.path, "r", encoding="utf-8") as f:
            data = json.load(f)

        text = self._flatten(data)

        return [
            Document(
                page_content=text,
                metadata={"source": self.path}
            )
        ]

    def _flatten(self, obj, prefix: str = "") -> str:
        """Recursively flatten a JSON object into readable key: value lines."""
        lines = []

        if isinstance(obj, dict):
            for key, value in obj.items():
                full_key = f"{prefix}.{key}" if prefix else key
                lines.append(self._flatten(value, prefix=full_key))

        elif isinstance(obj, list):
            for index, item in enumerate(obj):
                full_key = f"{prefix}[{index}]"
                lines.append(self._flatten(item, prefix=full_key))

        else:
            lines.append(f"{prefix}: {obj}")

        return "\n".join(lines)
