"""Text file ingestor using native Python file operations."""

from typing import List
from .ingestor_interface import IngestorInterface
from .quote_model import QuoteModel


class TextIngestor(IngestorInterface):
    """Ingest quotes from plain text files.

    This class handles parsing of TXT files that contain quotes in the
    format: "body" - author (one quote per line).
    """

    allowed_extensions = ['txt']

    @classmethod
    def parse(cls, path: str) -> List[QuoteModel]:
        """Parse a text file and return QuoteModel objects.

        Args:
            path: Path to the text file.

        Returns:
            A list of QuoteModel objects from the text file.

        Raises:
            Exception: If the file cannot be ingested or parsed.
        """
        if not cls.can_ingest(path):
            raise Exception(f'Cannot ingest file: {path}')

        quotes = []
        try:
            with open(path, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if line and ' - ' in line:
                        parts = line.split(' - ')
                        if len(parts) == 2:
                            body = parts[0].strip().strip('"')
                            author = parts[1].strip()
                            if body and author:
                                quotes.append(QuoteModel(body, author))
        except Exception as e:
            raise Exception(f'Error parsing text file {path}: {str(e)}')

        return quotes
