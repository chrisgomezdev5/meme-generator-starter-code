# Meme Generator

A multimedia application for dynamically generating memes by overlaying quotes on images. This project demonstrates object-oriented programming, working with various file types, and building both CLI and web applications in Python.

## Overview

The Meme Generator application can:
- Load quotes from various file formats (PDF, DOCX, CSV, TXT)
- Load and manipulate images using Pillow
- Generate memes by overlaying quotes on images
- Provide both a command-line interface and a Flask web application

## Project Structure

```
src/
├── QuoteEngine/           # Module for ingesting quotes from various file formats
│   ├── __init__.py
│   ├── quote_model.py     # QuoteModel class for representing quotes
│   ├── ingestor_interface.py  # Abstract base class for ingestors
│   ├── csv_ingestor.py    # CSV file ingestor using pandas
│   ├── docx_ingestor.py   # DOCX file ingestor using python-docx
│   ├── pdf_ingestor.py    # PDF file ingestor using pdftotext CLI
│   ├── text_ingestor.py   # TXT file ingestor using native Python
│   └── ingestor.py        # Main Ingestor class (strategy pattern)
├── MemeEngine/            # Module for creating memes
│   ├── __init__.py
│   └── meme_engine.py     # MemeEngine class for image manipulation
├── app.py                 # Flask web application
├── meme.py                # Command-line interface
├── templates/             # HTML templates for Flask
│   ├── base.html
│   ├── meme.html
│   └── meme_form.html
└── _data/                 # Sample data
    ├── DogQuotes/         # Sample quote files
    └── photos/dog/        # Sample images
```

## Setup Instructions

### Prerequisites

- Python 3.7 or higher
- xpdf command-line tools (for PDF processing)

#### Installing xpdf

**Windows:**
1. Download the Windows command-line tools from [xpdfreader.com](https://www.xpdfreader.com/download.html)
2. Unzip the files to a location of your choice
3. Add the `bin32` or `bin64` folder path to your system PATH environment variable

**Mac:**
```bash
brew install xpdf
```

**Linux:**
```bash
sudo apt-get install -y xpdf
```

### Installation

1. Clone or download this repository

2. Create a virtual environment:
```bash
python -m venv venv
```

3. Activate the virtual environment:
- Windows: `venv\Scripts\activate`
- Mac/Linux: `source venv/bin/activate`

4. Install required dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Command-Line Interface

Generate a random meme:
```bash
python src/meme.py
```

Generate a meme with a specific image:
```bash
python src/meme.py --path "path/to/image.jpg"
```

Generate a meme with a custom quote:
```bash
python src/meme.py --path "path/to/image.jpg" --body "Your quote here" --author "Author Name"
```

**Arguments:**
- `--path`: Path to an image file (optional)
- `--body`: Quote text to add to the image (optional, requires --author)
- `--author`: Quote author (required if --body is provided)

### Web Application

1. Start the Flask server:
```bash
python src/app.py
```

2. Open your browser and navigate to: `http://localhost:5000`

3. Features:
   - **Home Page**: Click "Random" to generate a meme with a random image and quote
   - **Creator**: Click "Creator" to make a custom meme by providing an image URL, quote, and author

## Module Documentation

### QuoteEngine Module

The QuoteEngine module is responsible for ingesting quotes from various file formats.

#### QuoteModel
Represents a quote with a body and author.

**Example:**
```python
from QuoteEngine import QuoteModel

quote = QuoteModel("To be or not to be", "Shakespeare")
print(quote)  # Output: "To be or not to be" - Shakespeare
```

#### Ingestor Classes
Each ingestor handles a specific file format:

- **CSVIngestor**: Parses CSV files with 'body' and 'author' columns using pandas
- **DocxIngestor**: Parses DOCX files using python-docx
- **PDFIngestor**: Parses PDF files using pdftotext CLI utility via subprocess
- **TextIngestor**: Parses plain text files using native Python file operations

**Example:**
```python
from QuoteEngine import Ingestor

# Automatically selects the appropriate ingestor based on file extension
quotes = Ingestor.parse('./path/to/quotes.csv')
for quote in quotes:
    print(quote)
```

#### IngestorInterface
Abstract base class that defines the interface all ingestors must implement:
- `can_ingest(cls, path: str) -> bool`: Check if file can be ingested
- `parse(cls, path: str) -> List[QuoteModel]`: Parse file and return quotes

**Dependencies:**
- pandas (for CSV parsing)
- python-docx (for DOCX parsing)
- subprocess (for PDF parsing via pdftotext)

### MemeEngine Module

The MemeEngine module handles image manipulation and meme creation.

#### MemeEngine
Creates memes by adding text to images using Pillow.

**Example:**
```python
from MemeEngine import MemeEngine

meme = MemeEngine('./output')
path = meme.make_meme(
    img_path='./dog.jpg',
    text='Such code',
    author='Doge',
    width=500
)
print(f'Meme saved to: {path}')
```

**Features:**
- Loads images in various formats (JPEG, PNG, etc.)
- Resizes images proportionally to a maximum width (default 500px)
- Adds quote text and author with outline for visibility
- Saves the result as a JPEG file
- Handles errors gracefully with descriptive messages

**Dependencies:**
- Pillow (PIL) for image manipulation

## Error Handling

The application includes comprehensive error handling:

- **Invalid file types**: Raises exceptions with descriptive messages
- **Missing required data**: Validates user input and provides feedback
- **File I/O errors**: Catches and reports file access issues
- **Network errors**: Handles image download failures gracefully
- **Temporary file cleanup**: Ensures temp files are removed even on errors

## Development

### Code Style

All code follows PEP 8 style guidelines:
- Clear, descriptive variable and function names
- Proper docstrings for all classes and methods
- Type hints for function parameters and returns
- DRY (Don't Repeat Yourself) principles

### Testing Quote Files

Sample quote files are provided in different formats:
- TXT: `src/_data/DogQuotes/DogQuotesTXT.txt`
- CSV: `src/_data/DogQuotes/DogQuotesCSV.csv`
- DOCX: `src/_data/DogQuotes/DogQuotesDOCX.docx`
- PDF: `src/_data/DogQuotes/DogQuotesPDF.pdf`

Format for quotes: `"quote body" - author` or CSV with body,author columns

## License

This project is part of the Udacity Intermediate Python course.

## Acknowledgments

- Sample dog images and quotes provided by Udacity
- Built with Flask, Pillow, pandas, and python-docx
