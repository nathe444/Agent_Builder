from typing import List

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
import trafilatura
from langchain_core.documents import Document

from app.ingestion.loaders.base import BaseLoader


class WebLoader(BaseLoader):
    """
    Loads and extracts clean, readable content from a web page.

    Uses trafilatura to strip navigation, ads, boilerplate, and scripts,
    keeping only the main article/body content plus useful metadata.
    Falls back to LangChain's WebBaseLoader if extraction fails.
    """

    def __init__(self, url: str, include_comments: bool = False, include_tables: bool = True):
        self.url = url
        self.include_comments = include_comments
        self.include_tables = include_tables

    def load(self) -> List[Document]:
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')

        with webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options) as driver:
            driver.get(self.url)
            downloaded = driver.page_source
    
        if downloaded is None:
            return self._fallback_load()

        content = trafilatura.extract(
            downloaded,
            include_comments=self.include_comments,
            include_tables=self.include_tables,
            include_links=False,
            favor_recall=True,
        )

        if not content or not content.strip():
            return self._fallback_load()

        metadata = trafilatura.extract_metadata(downloaded)

        doc_metadata = {
            "source": self.url,
            "title": metadata.title if metadata else None,
            "author": metadata.author if metadata else None,
            "date": metadata.date if metadata else None,
            "description": metadata.description if metadata else None,
            "sitename": metadata.sitename if metadata else None,
        }
        # drop Nones so downstream vectorstores/embeddings don't choke on nulls
        doc_metadata = {k: v for k, v in doc_metadata.items() if v is not None}

        return [Document(page_content=content, metadata=doc_metadata)]

    def _fallback_load(self) -> List[Document]:
        from langchain_community.document_loaders import WebBaseLoader

        loader = WebBaseLoader(self.url)
        docs = loader.load()
        for doc in docs:
            doc.metadata.setdefault("source", self.url)
        return docs