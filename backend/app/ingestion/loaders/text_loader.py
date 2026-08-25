from langchain_community.document_loaders import TextLoader

from app.ingestion.loaders.base import BaseLoader


class TXTLoader(BaseLoader):

    def __init__(self, path: str):
        self.path = path

    def load(self):
        loader = TextLoader(self.path)
        return loader.load()