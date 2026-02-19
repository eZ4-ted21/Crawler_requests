import re
from bs4 import BeautifulSoup
from Downloaders.dl_strat import Downloader
from DataModels.model import DataModel


class Extract():
    """
    A class that represents the scraper strategy.

    Attributes :
        url (str) : The url to scrape.

    Methods :
        Execute() : the method that executes scraping process for all pages.
        getDataPerPage() : the method for scraping data for each page.
        getNextUrl() : the method for getting next url.
        validateData() : the method for pydantic data type validation.
        getTitile() : the method for fetching title for each product.
        getURL() : the method for fetching url for each product.
        getPrice() : the method for fetching price for each product.
    """

    def __init__(self, url : str):
        """
        Initialize a new instance of a class with nextUrl, page, rank and a downloader.

        Args :
            url (str) : The very first page URL.

        Attributes :
            rank (int) : represents the arrangements of products.
            page (int) : represents the page number.
            nextUrl : The URL to be scrape. changes its value when navigating to next page.
            downloader : Represents the downloader method.
        """
        self.rank = 1
        self.page = 1
        self.nextUrl = url
        self.downloder = Downloader()

    def execute(self) -> list[dict]:
        """
        Saves Data scraped from multiple pages.

        Returns list of data scraped from multiple pages.

        Attributes :
            dataAllPage (list) : an empty list that represents as a temporary storage for scraped data.

        Behaviour :
            - Calls download method from Downloader class with the url to scrape.
            - Calls getDataPerPage method to fetch data.
            - Store all scraped data into dataAllPage.
            - Increments page number when scraping in previous page is successful.
            - Stops the loop when scraping is either done or unsuccessful.
        """
        dataAllPage : list = []

        while True:
            try:
                if not self.nextUrl:
                    break
                
                print(f'Requesting on page : {self.page}')
                rawData = self.downloder.download(self.nextUrl)
                if not rawData: 
                    break

                dataPerPage = self.getDataPerPage(rawData)
                if not dataPerPage: 
                    break

                dataAllPage.append({f'page {self.page}':dataPerPage})
                self.page+=1
            except Exception as e:
                print(f'[x] Download Failure excepteion : {e}.')
        return dataAllPage
        
    def getNextUrl(self, soup) -> str:
        """
        Navigate to html element where next url can be found.

        Returns next URL.

        Args : 
            soup (BeautifulSoup) : the html source that holds data.

        Attributes :
            tag (str) : represents the specific element where next url can be fetch.

        Behaviour :
            - Navigate to an html element and check if the next url exist.
        """
        try:
            self.nextUrl = None
            tag = soup.find('a',{'class':'next page-number'}) or soup.find('a', {'class':'pagination__item pagination__item--next pagination__item-arrow motion-reduce'})
            if tag and tag.has_attr('href'):
                url = tag['href']
                if not 'http' in url:
                    url = f'https://urbangadgets.ph/{url}'
                self.nextUrl = url
        except Exception as e:
            print(f'[x] Error ecounterd while fetching next url from page : {self.page}.')
        return self.nextUrl
        
    def getDataPerPage(self, rawData : str) -> list[dict]:
        """
        Gets all product data in a page.

        Returns list of product data in a single page.

        Args :
            rawData (str) : the html source for a single page.

        Attributes :
            soup (BeautifulSoup) : the html source.
            dataPerPage (list) : represents the list of data in a single page.
            tags (BeautifulSoup) : the list of html elements that holds data per product.
            dataPerRank (dict) : represents the data of a product.
            rank (int) : the rank of each product.

        Behaviour :
            - Calls getNextUrl method with the parameter soup.
            - Finds all html element that holds data for each product.
            - Loops through list of html elements for all product.
            - Calls validateData method.
            - Saves data to dataPerpage.
        """
        soup = BeautifulSoup(rawData, 'html.parser')
        self.nextUrl = self.getNextUrl(soup)
        dataPerPage = []

        tags = soup.find_all("div",{'class':'product-card product-card-style-standard'})
        
        if tags:
            for tag in tags:

                #get data with data type validation 
                _data = self.validateData(tag)

                dataPerRank = {
                    f"Rank : {self.rank}" : {
                        "title" : _data.title,
                        "url" : _data.url,
                        "price": _data.price
                        }
                }
                dataPerPage.append(dataPerRank)
                self.rank +=1
        return dataPerPage
    
    def validateData(self, tag : BeautifulSoup):
        """
        Validates data type from Pydantic Model.

        Returns Data for a specific product.

        Args :
            tag (BeautifulSoup) : represents the group of html elements that holds data for a specific product.

        Attributes :
            data (Pydantic) : new instance of a class Data.

        Behaviour :
            - Calls methods getTitle, getURL and getPrice
            - Validates value if data type is correct using pydantic.
        """
        return DataModel(
                    title = self.getTitle(tag),
                    url = self.getUrl(tag),
                    price = self.getPrice(tag)
                )
    

    def getTitle(self, tag : BeautifulSoup) -> str:
        """
        Naviagates and check if title exist in a target html element.

        Returns the title of a product.

        Args :
            tag (BeautifulSoup) : the html element for a product.
        
        Attributes :
            title (str) : represents the title or product name of a product.
            titleTag (str) : represents the html element where title can be found.

        Behaviour :
            - Navigates to a specific tag where title of the product can be found.
            - fetch the title of a product.
        """
        try:
            title = 'Not Found'
            titleTag = tag.find('p',{'class':'name product-title woocommerce-loop-product__title'}) or tag.find('a',{'class':'reversed-link'})
            if titleTag:
                title = titleTag.get_text().strip()
        except Exception as e:
            print(f'[x] Unhandled exception while fetching title on rank-{self.rank}: {e}')
        return title

    def getUrl(self, tag : BeautifulSoup) -> str:
        """
        Navigate to html tag where url of a specific product can be found.

        Returns the URL of a specific product.

        Args :
            tag (BeautifulSoup) : represents the specific group of elements that holds data for a single product.

        Attribute :
            url (str) : represents the url of a specific product.
            urlTag (BeautifulSoup) : represents the html element where url can be found.

        Behaviour : 
            - Navigate to a specific html element where url of a specific product can be found.
            - Check if the href attribute that holds the url exist in the target html element.
            - fetch the URL from html tag.
        """
        try:
            url = 'Not Found'
            urlTag = tag.find('a',{'class':'reversed-link'})
            if urlTag and urlTag.has_attr('href'):
                url = urlTag['href']
                if not 'https:' in url:
                    url = f'https://urbangadgets.ph{url}'
        except Exception as e:
            print(f'[x] Unhandled exception while fetching url on rank-{self.rank}: {e}')
        return url
    
    def getPrice(self, tag : BeautifulSoup) ->str:
        """
        Navigates to a specific html element where price can be found.

        Returns the price of a specific product.

        Args :
            tag (BeautifulSoup) : represents the group of html elements that holds data for a specific product.

        Attributes :
            price (str) : represents the price for a specific product.
            priceTag (BeautifulSoup) : the target html where price can be found.

        Behaviour :
            - Navigate to a specific tag that holds the price.
            - fetch the price from html tag.
        """
        try:
            price : str = '0.00'
            priceTag = tag.find('span',{'class':'price'}) or tag.find('span', {'class':'f-price-item f-price-item--sale'})
            if priceTag:
                price = priceTag.text
        except Exception as e:
            print(f'[x] Unhandled exception while fetching price on rank-{self.rank}: {e}')
        return price