"""DOCX file ingestor using python-docx library."""

from typing import List
import docx
from .ingestor_interface import IngestorInterface
from .quote_model import QuoteModel


class DocxIngestor(IngestorInterface):
    """Ingest quotes from DOCX files using python-docx.

    This class handles parsing of DOCX files that contain quotes in the
    format: "body" - author (one quote per paragraph).
    """

    allowed_extensions = ['docx']

    @classmethod
    def parse(cls, path: str) -> List[QuoteModel]:
        """Parse a DOCX file and return QuoteModel objects.

        Args:
            path: Path to the DOCX file.

        Returns:
            A list of QuoteModel objects from the DOCX file.

        Raises:
            Exception: If the file cannot be ingested or parsed.
        """
        if not cls.can_ingest(path):
            raise Exception(f'Cannot ingest file: {path}')

        quotes = []
        try:
            doc = docx.Document(path)
            
            for paragraph in doc.paragraphs:
                text = paragraph.text.strip()
                if text and ' - ' in text:
                    parts = text.split(' - ')
                    if len(parts) == 2:
                        body = parts[0].strip().strip('"')
                        author = parts[1].strip()
                        if body and author:
                            quotes.append(QuoteModel(body, author))
        except Exception as e:
            raise Exception(f'Error parsing DOCX file {path}: {str(e)}')

        return quotes
