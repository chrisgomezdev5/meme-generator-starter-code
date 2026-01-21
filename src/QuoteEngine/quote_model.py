"""QuoteModel class for representing quotes with body and author."""


class QuoteModel:
    """Encapsulate quote body and author data.

    A QuoteModel represents a single quote with a body (the quote text)
    and an author (who said it).
    """

    def __init__(self, body: str, author: str):
        """Initialize a QuoteModel.

        Args:
            body: The quote text.
            author: The author of the quote.
        """
        self.body = body
        self.author = author

    def __repr__(self) -> str:
        """Return a machine-readable representation of the QuoteModel.

        Returns:
            A string representation showing the class and its attributes.
        """
        return f'QuoteModel(body="{self.body}", author="{self.author}")'

    def __str__(self) -> str:
        """Return a human-readable string representation of the quote.

        Returns:
            A formatted string in the format: "body" - author
        """
        return f'"{self.body}" - {self.author}'
