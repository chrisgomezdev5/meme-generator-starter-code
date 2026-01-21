"""Abstract base class for quote ingestors."""

from abc import ABC, abstractmethod
from typing import List
from .quote_model import QuoteModel


class IngestorInterface(ABC):
    """Define interface for quote ingestors.

    This abstract base class defines the contract that all concrete
    ingestor classes must follow. Each ingestor is responsible for
    parsing quotes from a specific file format.
    """

    allowed_extensions = []

    @classmethod
    def can_ingest(cls, path: str) -> bool:
        """Check if the file can be ingested by this ingestor.

        Args:
            path: Path to the file to check.

        Returns:
            True if the file extension is supported, False otherwise.
        """
        ext = path.split('.')[-1].lower()
        return ext in cls.allowed_extensions

    @classmethod
    @abstractmethod
    def parse(cls, path: str) -> List[QuoteModel]:
        """Parse the file and return a list of QuoteModel objects.

        This method must be implemented by all concrete ingestor classes.

        Args:
            path: Path to the file to parse.

        Returns:
            A list of QuoteModel objects extracted from the file.

        Raises:
            Exception: If the file cannot be ingested.
        """
        pass
