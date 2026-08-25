import io

import fitz  # pymupdf
from langchain_core.documents import Document

from app.ingestion.loaders.base import BaseLoader


class PDFLoader(BaseLoader):

    def __init__(self, path: str):
        self.path = path

    def load(self) -> list[Document]:
        doc = fitz.open(self.path)
        documents = []

        for i, page in enumerate(doc):
            text = page.get_text().strip()

            # No text layer found — fall back to OCR
            if not text:
                text = self._ocr_page(page)

            if text:
                documents.append(
                    Document(
                        page_content=text,
                        metadata={
                            "page": i,
                            "source": self.path
                        }
                    )
                )

        doc.close()
        return documents

    def _ocr_page(self, page) -> str:
        """Render the page as a high-res image and run Tesseract OCR on it."""
        try:
            import pytesseract
            from PIL import Image

            # 2x scale for better OCR accuracy
            mat = fitz.Matrix(2, 2)
            pix = page.get_pixmap(matrix=mat)
            img = Image.open(io.BytesIO(pix.tobytes("png")))
            return pytesseract.image_to_string(img).strip()

        except Exception as e:
            print(f"OCR failed for page: {e}")
            return ""
