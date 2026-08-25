from langchain_community.document_loaders import Docx2txtLoader

from app.ingestion.loaders.base import BaseLoader


class DOCXLoader(BaseLoader):

    def __init__(self, path: str):
        self.path = path

    def load(self):
        loader = Docx2txtLoader(self.path)
        return loader.load()