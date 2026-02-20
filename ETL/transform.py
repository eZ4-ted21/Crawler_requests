import re

class Transformer():
    """
    a class that represents data transformation
    
    methods :
        transformPage() : clean product data for page info
        transformRank() : clean product data for product rank
        transformTitle() : clean product data for title
        transformURL() : clean product data for URL
        transformURL() : clean product data for price
    """

    def __init__(self):
        """
        Initialize a new instance of a class.
        """
        pass
    
    def transformPage(self, page : str) -> str:
        """
        Cleaning data with the use of regular expression to filter numeric value only.

        Returns page number in a string data type.
        Args :
            page (str) : the page indicator where product data can be found
        """
        return re.sub(r'[^0-9]', '', page)
    
    def transformRank(self, rank:str) -> str:
        """
        Cleaning data with the use of regular expression to filter numeric value only.

        Returns rank number in a string data type.
        Args:
            rank (str) : the rank iindicator of a product.
        """
        return re.sub(r'[^0-9]', '', rank)
    
    def transformTitle(self, title:str) ->str:
        """
        Cleaning data for title
        TODO:// implement data cleaning mechanism when needed.
        Returns Title in a string data type.
        Args:
            title(str): represents the product name for each item.
        """
        return title
    
    def transformURL(self, url:str) ->str:
        """
        Cleaning data for URL

        TODO:// implement data cleaning mechanism when needed
        Returns URL in a string format
        Args:
            url (str) : represents the product url for each item
        """
        return url
    
    def transformPrice(self, price):
        """
        Cleaning product price using regular expression to filter numeric and '.' symbol only.

        Returns price in a string data type.

        Args:
            price (str) : represents the price for each item.
        """
        return re.sub(r'[^0-9.]', '', price)
