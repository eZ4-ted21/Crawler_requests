import re

class Transformer:
    """
    a class that represents data transformation
    
    methods :
        transform_page() : clean product data for page info
        transform_rank() : clean product data for product rank
        transform_title() : clean product data for title
        transform_url() : clean product data for URL
        transform_price() : clean product data for price
    """

    def __init__(self):
        """
        Initialize a new instance of a class.
        """
        pass

    @staticmethod
    def transform_page(page : str) -> str:
        """
        Cleaning data with the use of regular expression to filter numeric value only.

        Returns page number in a string data type.
        Args :
            page (str) : the page indicator where product data can be found
        """
        return re.sub(r'[^0-9]', '', page)

    @staticmethod
    def transform_rank(rank:str) -> str:
        """
        Cleaning data with the use of regular expression to filter numeric value only.

        Returns rank number in a string data type.
        Args:
            rank (str) : the rank indicator of a product.
        """
        return re.sub(r'[^0-9]', '', rank)

    @staticmethod
    def transform_title(title:str) ->str:
        """
        Cleaning data for title
        TODO:// implement data cleaning mechanism when needed.
        Returns Title in a string data type.
        Args:
            title(str): represents the product name for each item.
        """
        return title

    @staticmethod
    def transform_url(url:str) ->str:
        """
        Cleaning data for URL

        TODO:// implement data cleaning mechanism when needed
        Returns URL in a string format
        Args:
            url (str) : represents the product url for each item
        """
        return url

    @staticmethod
    def transform_price(price):
        """
        Cleaning product price using regular expression to filter numeric and '.' symbol only.

        Returns price in a string data type.

        Args:
            price (str) : represents the price for each item.
        """
        return re.sub(r'[^0-9.]', '', price)
