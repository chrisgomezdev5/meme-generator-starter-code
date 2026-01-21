"""QuoteEngine module for ingesting quotes from various file formats.

This module provides classes for parsing quotes from different file types
including CSV, DOCX, PDF, and TXT files.
"""

from .quote_model import QuoteModel
from .ingestor_interface import IngestorInterface
from .csv_ingestor import CSVIngestor
from .docx_ingestor import DocxIngestor
from .pdf_ingestor import PDFIngestor
from .text_ingestor import TextIngestor
from .ingestor import Ingestor

__all__ = [
    'QuoteModel',
    'IngestorInterface',
    'CSVIngestor',
    'DocxIngestor',
    'PDFIngestor',
    'TextIngestor',
    'Ingestor'
]
