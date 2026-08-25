from langchain_community.document_loaders import CSVLoader

from app.ingestion.loaders.base import BaseLoader


class CSVDocumentLoader(BaseLoader):

    def __init__(self, path: str):
        self.path = path

    def load(self):
        loader = CSVLoader(
            file_path=self.path
        )

        return loader.load()