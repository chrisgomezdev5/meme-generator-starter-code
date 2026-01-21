"""Flask web application for generating memes.

This application provides a web interface for creating random memes
or custom memes with user-provided images and quotes.
"""

import random
import os
import requests
from flask import Flask, render_template, abort, request
from QuoteEngine import Ingestor, QuoteModel
from MemeEngine import MemeEngine

app = Flask(__name__)

# Get the directory where this script is located
script_dir = os.path.dirname(os.path.abspath(__file__))
static_dir = os.path.join(os.path.dirname(script_dir), 'static')
meme = MemeEngine(static_dir)


def setup():
    """Load all resources for the application.

    This function loads all quotes from various file formats and
    discovers all available dog images.

    Returns:
        A tuple of (quotes, imgs) where quotes is a list of QuoteModel
        objects and imgs is a list of image file paths.
    """
    # Get the directory where this script is located
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    quote_files = [os.path.join(script_dir, '_data/DogQuotes/DogQuotesTXT.txt'),
                   os.path.join(script_dir, '_data/DogQuotes/DogQuotesDOCX.docx'),
                   os.path.join(script_dir, '_data/DogQuotes/DogQuotesPDF.pdf'),
                   os.path.join(script_dir, '_data/DogQuotes/DogQuotesCSV.csv')]

    # Use the Ingestor class to parse all files
    quotes = []
    for file in quote_files:
        try:
            quotes.extend(Ingestor.parse(file))
        except Exception as e:
            print(f'Error loading quotes from {file}: {e}')

    images_path = os.path.join(script_dir, "_data/photos/dog/")

    # Find all images in the directory
    imgs = []
    for root, dirs, files in os.walk(images_path):
        imgs = [os.path.join(root, name) for name in files]

    return quotes, imgs


quotes, imgs = setup()


@app.route('/')
def meme_rand():
    """Generate a random meme.

    This route selects a random image and quote, generates a meme,
    and displays it to the user.

    Returns:
        Rendered template with the generated meme.
    """
    # Select a random image and quote
    img = random.choice(imgs)
    quote = random.choice(quotes)
    
    path = meme.make_meme(img, quote.body, quote.author)
    return render_template('meme.html', path=path)


@app.route('/create', methods=['GET'])
def meme_form():
    """Display the meme creation form.

    Returns:
        Rendered template with the meme creation form.
    """
    return render_template('meme_form.html')


@app.route('/create', methods=['POST'])
def meme_post():
    """Create a user-defined meme from form data.

    This route receives an image URL, quote body, and author from
    a form submission, downloads the image, generates a meme, and
    cleans up temporary files.

    Returns:
        Rendered template with the generated meme.
    """
    # Get form data
    image_url = request.form.get('image_url')
    body = request.form.get('body', '')
    author = request.form.get('author', '')

    # Validate inputs
    if not image_url:
        return render_template('meme_form.html', 
                             error='Image URL is required')
    if not body:
        return render_template('meme_form.html', 
                             error='Quote body is required')
    if not author:
        return render_template('meme_form.html', 
                             error='Author is required')

    # Download image from URL to a temporary file
    tmp_img_path = None
    try:
        response = requests.get(image_url, timeout=10)
        response.raise_for_status()
        
        # Save to temporary file
        tmp_img_path = f'./tmp/downloaded_{random.randint(0, 1000000)}.jpg'
        os.makedirs('./tmp', exist_ok=True)
        
        with open(tmp_img_path, 'wb') as img_file:
            img_file.write(response.content)
        
        # Generate the meme
        path = meme.make_meme(tmp_img_path, body, author)
        
    except requests.RequestException as e:
        return render_template('meme_form.html', 
                             error=f'Error downloading image: {str(e)}')
    except Exception as e:
        return render_template('meme_form.html', 
                             error=f'Error creating meme: {str(e)}')
    finally:
        # Clean up temporary file
        if tmp_img_path and os.path.exists(tmp_img_path):
            try:
                os.remove(tmp_img_path)
            except Exception:
                pass

    return render_template('meme.html', path=path)


if __name__ == "__main__":
    app.run()
