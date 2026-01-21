"""CSV file ingestor using pandas library."""

from typing import List
import pandas as pd
from .ingestor_interface import IngestorInterface
from .quote_model import QuoteModel


class CSVIngestor(IngestorInterface):
    """Ingest quotes from CSV files using pandas.

    This class handles parsing of CSV files that contain quotes with
    'body' and 'author' columns.
    """

    allowed_extensions = ['csv']

    @classmethod
    def parse(cls, path: str) -> List[QuoteModel]:
        """Parse a CSV file and return QuoteModel objects.

        Args:
            path: Path to the CSV file.

        Returns:
            A list of QuoteModel objects from the CSV file.

        Raises:
            Exception: If the file cannot be ingested or parsed.
        """
        if not cls.can_ingest(path):
            raise Exception(f'Cannot ingest file: {path}')

        quotes = []
        try:
            df = pd.read_csv(path, header=0)
            
            for _, row in df.iterrows():
                if 'body' in row and 'author' in row:
                    body = str(row['body']).strip()
                    author = str(row['author']).strip()
                    if body and author:
                        quotes.append(QuoteModel(body, author))
        except Exception as e:
            raise Exception(f'Error parsing CSV file {path}: {str(e)}')

        return quotes
