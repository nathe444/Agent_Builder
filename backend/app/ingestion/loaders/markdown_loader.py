from langchain_community.document_loaders import TextLoader

from app.ingestion.loaders.base import BaseLoader


class MarkdownLoader(BaseLoader):

    def __init__(self, path: str):
        self.path = path

    def load(self):
        loader = TextLoader(
            self.path,
            encoding="utf-8"
        )

        return loader.load()