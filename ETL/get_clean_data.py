from typing import Any

from ETL.transform import Transformer

class CleanData:
    """
    a class that represents data transformation
    
    methods :
        _getListData() : store all rankings data from one page in a list
        _getProductData() : packing each product data into a dictionary
    """

    def __init__(self, scraped_data):
        """
        Initialize a new instance of a class.
        """
        self.scraped_data = scraped_data
        self.transformer = Transformer()

    def get_list_data(self) -> list[Any] | None:
        """
        TODO://
        """
        try:
            data = []
            for page in self.scraped_data:
                page_key = list(page.keys())[0]
                page_data = page[page_key]
                for pd in page_data:
                    pd_key = list(pd.keys())[0]
                    prd_data = pd[pd_key]
                    data.append(self._get_product_data(page_key, pd_key, prd_data))
            return data
        except Exception as e:
            print(f'[x] Unhandled Exception encountered while getting list of Data {e}')

    
    def _get_product_data(self, page_key: str, rd_key : str, prd_data: dict) -> dict[str, str | Any] | None:
        """
        Packing all clean data from one product into a dictionary.

        Returns Product Data
        
        Args:
            page_key (str) : represents the page indicator where a product can be found
            rd_key (str) : represents the product rank
            prd_data(dict) : the product data of each item
        """
        try:
            product_data = {
                'PAGE' : self.transformer.transform_page(page_key),
                'RANK': self.transformer.transform_rank(rd_key),
                'TITLE' :self.transformer.transform_title(prd_data.get('title')),
                'URL' : self.transformer.transform_url(prd_data.get('url')),
                'PRICE' : self.transformer.transform_price(prd_data.get('price'))
            }
            return product_data
        except Exception as e:
            print(f'x] Unhandled Exception encountered while getting Data per Rank {e}')
