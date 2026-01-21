"""Command-line interface for generating memes.

This module provides a CLI tool for generating memes from images and
quotes. Users can specify custom images and quotes or use random ones.
"""

import os
import random
import argparse
from QuoteEngine import Ingestor, QuoteModel
from MemeEngine import MemeEngine


def generate_meme(path=None, body=None, author=None):
    """Generate a meme given a path and a quote.

    If no path is provided, a random image is selected. If no body
    is provided, a random quote is selected.

    Args:
        path: Path to an image file (optional).
        body: Quote body text (optional).
        author: Quote author (optional, required if body is provided).

    Returns:
        Path to the generated meme image.

    Raises:
        Exception: If body is provided without an author.
    """
    img = None
    quote = None

    if path is None:
        # Get the directory where this script is located
        script_dir = os.path.dirname(os.path.abspath(__file__))
        images = os.path.join(script_dir, "_data/photos/dog/")
        imgs = []
        for root, dirs, files in os.walk(images):
            imgs.extend([os.path.join(root, name) for name in files 
                        if name.lower().endswith(('.jpg', '.jpeg', '.png'))])

        img = random.choice(imgs)
    else:
        img = path

    if body is None:
        # Get the directory where this script is located
        script_dir = os.path.dirname(os.path.abspath(__file__))
        quote_files = [os.path.join(script_dir, '_data/DogQuotes/DogQuotesTXT.txt'),
                       os.path.join(script_dir, '_data/DogQuotes/DogQuotesDOCX.docx'),
                       os.path.join(script_dir, '_data/DogQuotes/DogQuotesPDF.pdf'),
                       os.path.join(script_dir, '_data/DogQuotes/DogQuotesCSV.csv')]
        quotes = []
        for f in quote_files:
            try:
                quotes.extend(Ingestor.parse(f))
            except Exception as e:
                print(f'Error loading quotes from {f}: {e}')

        quote = random.choice(quotes)
    else:
        if author is None:
            raise Exception('Author Required if Body is Used')
        quote = QuoteModel(body, author)

    # Get the directory where this script is located
    script_dir = os.path.dirname(os.path.abspath(__file__))
    tmp_dir = os.path.join(os.path.dirname(script_dir), 'tmp')
    meme = MemeEngine(tmp_dir)
    path = meme.make_meme(img, quote.body, quote.author)
    return path


if __name__ == "__main__":
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description='Generate a meme')
    parser.add_argument('--path', type=str, default=None,
                       help='Path to an image file')
    parser.add_argument('--body', type=str, default=None,
                       help='Quote body to add to the image')
    parser.add_argument('--author', type=str, default=None,
                       help='Quote author to add to the image')
    
    args = parser.parse_args()
    
    try:
        print(generate_meme(args.path, args.body, args.author))
    except Exception as e:
        print(f'Error: {e}')
