"""MemeEngine class for generating memes from images and quotes."""

import os
import random
from PIL import Image, ImageDraw, ImageFont


class MemeEngine:
    """Create memes by adding text to images.

    This class handles loading images, resizing them, adding quote text
    and author information, and saving the result.
    """

    def __init__(self, output_dir: str):
        """Initialize the MemeEngine.

        Args:
            output_dir: Directory where generated memes will be saved.
        """
        self.output_dir = output_dir
        
        # Create output directory if it doesn't exist
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

    def make_meme(self, img_path: str, text: str, author: str, 
                  width: int = 500) -> str:
        """Generate a meme with quote text on an image.

        This method loads an image, resizes it proportionally to the
        specified width, adds the quote text and author, and saves
        the result to the output directory.

        Args:
            img_path: Path to the input image file.
            text: The quote text to add to the image.
            author: The author of the quote.
            width: Maximum width for the output image (default: 500px).

        Returns:
            The path to the generated meme image.

        Raises:
            Exception: If the image cannot be loaded or processed.
        """
        try:
            # Load the image
            img = Image.open(img_path)
            
            # Resize image if width is larger than specified
            if img.width > width:
                ratio = width / float(img.width)
                height = int(ratio * float(img.height))
                img = img.resize((width, height), Image.LANCZOS)
            
            # Prepare to draw text
            draw = ImageDraw.Draw(img)
            
            # Try to load a font, fall back to default if not available
            try:
                font_size = 20
                font = ImageFont.truetype('arial.ttf', font_size)
            except Exception:
                # Use default font if arial is not available
                font = ImageFont.load_default()
            
            # Format the quote text
            quote_text = f'"{text}"'
            author_text = f'- {author}'
            
            # Calculate text positions (random Y position for variety)
            img_width, img_height = img.size
            margin = 10
            y_position = random.randint(margin, img_height - 100)
            
            # Draw quote text with outline for better visibility
            text_color = (255, 255, 255)  # White
            outline_color = (0, 0, 0)  # Black
            
            # Draw text outline
            for adj_x in range(-2, 3):
                for adj_y in range(-2, 3):
                    draw.text((margin + adj_x, y_position + adj_y), 
                             quote_text, font=font, fill=outline_color)
            
            # Draw main text
            draw.text((margin, y_position), quote_text, 
                     font=font, fill=text_color)
            
            # Draw author text
            y_position += 25
            for adj_x in range(-2, 3):
                for adj_y in range(-2, 3):
                    draw.text((margin + adj_x, y_position + adj_y), 
                             author_text, font=font, fill=outline_color)
            
            draw.text((margin, y_position), author_text, 
                     font=font, fill=text_color)
            
            # Generate output filename
            out_filename = f'meme_{random.randint(0, 1000000)}.jpg'
            out_path = os.path.join(self.output_dir, out_filename)
            
            # Save the image
            img.save(out_path)
            
            return out_path
            
        except Exception as e:
            raise Exception(f'Error creating meme: {str(e)}')
