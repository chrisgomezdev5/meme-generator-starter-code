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

    def _load_image(self, img_path: str) -> Image:
        """Load an image from disk.
        
        Args:
            img_path: Path to the input image file.
            
        Returns:
            Loaded PIL Image object.
        """
        return Image.open(img_path)

    def _resize_image(self, img: Image, max_width: int) -> Image:
        """Resize image to max width while maintaining aspect ratio.
        
        Args:
            img: PIL Image object to resize.
            max_width: Maximum width for the output image.
            
        Returns:
            Resized PIL Image object.
        """
        if img.width > max_width:
            ratio = max_width / float(img.width)
            height = int(ratio * float(img.height))
            img = img.resize((max_width, height), Image.LANCZOS)
        return img

    def _get_font(self, size: int = 20) -> ImageFont:
        """Load font, falling back to default if unavailable.
        
        Args:
            size: Font size in points.
            
        Returns:
            ImageFont object.
        """
        try:
            return ImageFont.truetype('arial.ttf', size)
        except Exception:
            return ImageFont.load_default()

    def _draw_text_with_outline(self, draw: ImageDraw, position: tuple,
                                 text: str, font: ImageFont):
        """Draw text with outline for visibility.
        
        Args:
            draw: ImageDraw object to draw on.
            position: (x, y) tuple for text position.
            text: Text string to draw.
            font: ImageFont to use for drawing.
        """
        x, y = position
        outline_color = (0, 0, 0)
        text_color = (255, 255, 255)

        for adj_x in range(-2, 3):
            for adj_y in range(-2, 3):
                draw.text((x + adj_x, y + adj_y), text,
                         font=font, fill=outline_color)
        draw.text(position, text, font=font, fill=text_color)

    def _get_random_position(self, img: Image, margin: int = 10) -> tuple:
        """Calculate random position for text placement.
        
        Args:
            img: PIL Image object to place text on.
            margin: Margin from edges in pixels.
            
        Returns:
            (x, y) tuple for text position.
        """
        max_y = img.height - 100
        y = random.randint(margin, max_y)
        return (margin, y)

    def _save_image(self, img: Image) -> str:
        """Save image to output directory with random filename.
        
        Args:
            img: PIL Image object to save.
            
        Returns:
            Path to the saved image file.
        """
        filename = f'meme_{random.randint(0, 1000000)}.jpg'
        out_path = os.path.join(self.output_dir, filename)
        img.save(out_path)
        return out_path

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
            # Load and resize
            img = self._load_image(img_path)
            img = self._resize_image(img, width)

            # Add text
            draw = ImageDraw.Draw(img)
            font = self._get_font()
            x, y = self._get_random_position(img)

            # Draw quote and author
            self._draw_text_with_outline(draw, (x, y), f'"{text}"', font)
            self._draw_text_with_outline(draw, (x, y + 25), f'- {author}', font)

            return self._save_image(img)
            
        except Exception as e:
            raise Exception(f'Error creating meme: {str(e)}')
