"""PDF file ingestor using pdftotext CLI utility."""

from typing import List
import subprocess
import os
import tempfile
from .ingestor_interface import IngestorInterface
from .quote_model import QuoteModel


class PDFIngestor(IngestorInterface):
    """Ingest quotes from PDF files using pdftotext CLI.

    This class handles parsing of PDF files by converting them to text
    using the pdftotext command-line utility, then parsing the text.
    """

    allowed_extensions = ['pdf']

    @classmethod
    def parse(cls, path: str) -> List[QuoteModel]:
        """Parse a PDF file and return QuoteModel objects.

        This method uses subprocess to call pdftotext, converts the PDF
        to a temporary text file, parses it, and cleans up the temp file.

        Args:
            path: Path to the PDF file.

        Returns:
            A list of QuoteModel objects from the PDF file.

        Raises:
            Exception: If the file cannot be ingested or parsed.
        """
        if not cls.can_ingest(path):
            raise Exception(f'Cannot ingest file: {path}')

        quotes = []
        tmp = None
        
        try:
            # Create a temporary file for the text output
            tmp = tempfile.NamedTemporaryFile(mode='w', delete=False, 
                                             suffix='.txt')
            tmp.close()
            
            # Call pdftotext to convert PDF to text
            subprocess.run(['pdftotext', '-layout', path, tmp.name],
                          check=True, capture_output=True)
            
            # Read the temporary text file
            with open(tmp.name, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if line and ' - ' in line:
                        parts = line.split(' - ')
                        if len(parts) == 2:
                            body = parts[0].strip().strip('"')
                            author = parts[1].strip()
                            if body and author:
                                quotes.append(QuoteModel(body, author))
        except subprocess.CalledProcessError as e:
            raise Exception(f'Error calling pdftotext for {path}: {str(e)}')
        except Exception as e:
            raise Exception(f'Error parsing PDF file {path}: {str(e)}')
        finally:
            # Clean up temporary file
            if tmp and os.path.exists(tmp.name):
                try:
                    os.remove(tmp.name)
                except Exception:
                    pass

        return quotes
