"""Main Ingestor class that encapsulates all ingestor strategies."""

from typing import List
from .ingestor_interface import IngestorInterface
from .quote_model import QuoteModel
from .csv_ingestor import CSVIngestor
from .docx_ingestor import DocxIngestor
from .pdf_ingestor import PDFIngestor
from .text_ingestor import TextIngestor


class Ingestor(IngestorInterface):
    """Encapsulate all ingestors and select the appropriate one.

    This class implements the strategy pattern to select the correct
    ingestor based on the file extension.
    """

    ingestors = [CSVIngestor, DocxIngestor, PDFIngestor, TextIngestor]

    @classmethod
    def parse(cls, path: str) -> List[QuoteModel]:
        """Parse a file using the appropriate ingestor.

        This method automatically selects the correct ingestor based on
        the file extension and delegates the parsing to that ingestor.

        Args:
            path: Path to the file to parse.

        Returns:
            A list of QuoteModel objects from the file.

        Raises:
            Exception: If no suitable ingestor is found for the file type.
        """
        for ingestor in cls.ingestors:
            if ingestor.can_ingest(path):
                return ingestor.parse(path)
        
        raise Exception(f'No compatible ingestor found for file: {path}')
