from app.ingestion.loaders.pdf_loader import PDFLoader
from app.ingestion.loaders.docx_loader import DOCXLoader
from app.ingestion.loaders.csv_loader import CSVDocumentLoader
from app.ingestion.loaders.markdown_loader import MarkdownLoader
from app.ingestion.loaders.text_loader import TXTLoader
from app.ingestion.loaders.web_loader import WebLoader
from app.ingestion.loaders.json_loader import JSONLoader



class LoaderFactory:

    @staticmethod
    def get_loader(
        source_type: str,
        file_path: str | None = None,
        source_value: str | None = None
    ):
        match source_type:

            case "pdf":
                return PDFLoader(file_path)

            case "docx" :
                return DOCXLoader(file_path)

            case "csv":
                return CSVDocumentLoader(file_path)

            case "txt":
                return TXTLoader(file_path)

            case "md":
                return MarkdownLoader(file_path)

            case "json":
                return JSONLoader(file_path)

            case "url":
                return WebLoader(source_value)

            case _:
                raise ValueError(
                    f"Unsupported document type: {source_type}"
                )