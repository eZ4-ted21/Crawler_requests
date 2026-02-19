from ETL.transform import Transformer

class CleanData():
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

    def _getListData(self) -> list[dict]:
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
                    data.append(self._getProductData(page_key, pd_key, prd_data))
        except Exception as e:
            print(f'[x] Unhandled Exeption encountered while getting list of Data {e}')
        return data
    
    def _getProductData(self, page_key: str, rd_key : str, prd_data: dict) -> dict:
        """
        Packing all clean data from one product into a dictionary.

        Returns Product Data
        
        Args:
            page_key (str) : represents the page indicator where a product can be found
            rd_key (str) : represents the product rank
            prd_data(dict) : the product data of each item
        Attributes:
            productData (dict) : represents the data per item with the title, url and price.
        """
        try:
            productData = {
                'PAGE' : self.transformer.transformPage(page_key),
                'RANK': self.transformer.transformRank(rd_key),
                'TITLE' :self.transformer.transformTitle(prd_data.get('title')),
                'URL' : self.transformer.transformURL(prd_data.get('url')),
                'PRICE' : self.transformer.transformPrice(prd_data.get('price'))
            }
        except Exception as e:
            print(f'x] Unhandled Exeption encountered while getting Data per Rank {e}')
        return productData