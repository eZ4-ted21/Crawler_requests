from typing import Any

from bs4 import BeautifulSoup

from Downloaders.dl_strat import Downloader
from DataModels.model import DataModel


class Extract:
    """
    A class that represents the scraper strategy.

    Attributes :
        url (str) : The url to scrape.

    Methods :
        execute() : the method that executes scraping process for all pages.
        get_data_per_page() : the method for scraping data for each page.
        get_next_url() : the method for getting next url.
        validateData() : the method for pydantic data type validation.
        get_title() : the method for fetching title for each product.
        get_url() : the method for fetching url for each product.
        get_price() : the method for fetching price for each product.
    """

    def __init__(self, url : str):
        """
        Initialize a new instance of a class with nextUrl, page, rank and a downloader.

        Args :
            url (str) : The very first page URL.

        Attributes :
            rank (int) : represents the arrangements of products.
            page (int) : represents the page number.
            nextUrl : The URL to be scraped. changes its value when navigating to next page.
            downloader : Represents the downloader method.
        """
        self.rank = 1
        self.page = 1
        self.next_url = url
        self.downloader = Downloader()

    def execute(self) -> list[dict]:
        """
        Saves Data scraped from multiple pages.

        Returns list of data scraped from multiple pages.

        Attributes :
            dataAllPage (list) : an empty list that represents as a temporary storage for scraped data.

        Behavior :
            - Calls download method from Downloader class with the url to scrape.
            - Calls getDataPerPage method to fetch data.
            - Store all scraped data into dataAllPage.
            - Increments page number when scraping in previous page is successful.
            - Stops the loop when scraping is either done or unsuccessful.
        """
        data_all_page : list = []

        while True:
            try:
                if not self.next_url:
                    break
                
                print(f'Requesting on page : {self.page}')
                raw_data = self.downloader.download(self.next_url)
                if not raw_data:
                    break

                data_per_page = self.get_data_per_page(raw_data)
                if not data_per_page:
                    break

                data_all_page.append({f'page {self.page}':data_per_page})
                self.page+=1
            except Exception as e:
                print(f'[x] Download Failure Exception : {e}.')
        return data_all_page
        
    def get_next_url(self, soup) -> str | None | Any:
        """
        Navigate to HTML element where next url can be found.

        Returns next URL.

        Args : 
            soup (BeautifulSoup) : the HTML source that holds data.

        Attributes :
            tag (str) : represents the specific element where next url can be fetched.

        Behavior :
            - Navigate to an HTML element and check if the next url exist.
        """
        try:
            self.next_url = None
            tag = soup.find('a',{'class':'next page-number'}) or soup.find('a', {'class':'pagination__item pagination__item--next pagination__item-arrow motion-reduce'})
            if tag and tag.has_attr('href'):
                url = tag['href']
                if not 'http' in url:
                    url = f'https://urbangadgets.ph/{url}'
                self.next_url = url
            return self.next_url
        except Exception as e:
            print(f'[x] Error encountered while fetching next url from page : {self.page} - {e}.')

        
    def get_data_per_page(self, raw_data : str) -> list[dict]:
        """
        Gets all product data in a page.

        Returns list of product data in a single page.

        Args :
            rawData (str) : the HTML source for a single page.

        Attributes :
            soup (BeautifulSoup) : the HTML source.
            dataPerPage (list) : represents the list of data in a single page.
            tags (BeautifulSoup) : the list of HTML elements that holds data per product.
            dataPerRank (dict) : represents the data of a product.
            rank (int) : the rank of each product.

        Behavior :
            - Calls getNextUrl method with the parameter soup.
            - Finds all HTML element that holds data for each product.
            - Loops through list of HTML elements for all product.
            - Calls validateData method.
            - Saves data to data_per_page.
        """
        soup = BeautifulSoup(raw_data, 'html.parser')
        self.next_url = self.get_next_url(soup)
        data_per_page = []

        tags = soup.find_all("div",{'class':'product-card product-card-style-standard'})
        
        if tags:
            for tag in tags:

                #get data with data type validation 
                _data = self.validate_data(tag)

                data_per_rank = {
                    f"Rank : {self.rank}" : {
                        "title" : _data.title,
                        "url" : _data.url,
                        "price": _data.price
                        }
                }
                data_per_page.append(data_per_rank)
                self.rank +=1
        return data_per_page
    
    def validate_data(self, tag):
        """
        Validates data type from Pydantic Model.

        Returns Data for a specific product.

        Args :
            tag (BeautifulSoup) : represents the group of HTML elements that holds data for a specific product.

        Attributes :
            data (Pydantic) : new instance of a class Data.

        Behavior :
            - Calls methods getTitle, getURL and getPrice
            - Validates value if data type is correct using pydantic.
        """
        return DataModel(
                    title = self.get_title(tag),
                    url = self.get_url(tag),
                    price = self.get_price(tag)
                )
    

    def get_title(self, tag) -> str | None | Any:
        """
        Navigates and check if title exist in a target HTML element.

        Returns the title of a product.

        Args :
            tag (BeautifulSoup) : the HTML element for a product.
        
        Attributes :
            title (str) : represents the title or product name of a product.
            titleTag (str) : represents the HTML element where title can be found.

        Behavior :
            - Navigates to a specific tag where title of the product can be found.
            - fetch the title of a product.
        """
        try:
            title = 'Not Found'
            title_tag = tag.find('p',{'class':'name product-title woocommerce-loop-product__title'}) or tag.find('a',{'class':'reversed-link'})
            if title_tag:
                title = title_tag.get_text().strip()
            return title
        except Exception as e:
            print(f'[x] Unhandled exception while fetching title on rank-{self.rank}: {e}')

    def get_url(self, tag : BeautifulSoup) -> str | None:
        """
        Navigate to HTML tag where url of a specific product can be found.

        Returns the URL of a specific product.

        Args :
            tag (BeautifulSoup) : represents the specific group of elements that holds data for a single product.

        Attribute :
            url (str) : represents the url of a specific product.
            urlTag (BeautifulSoup) : represents the HTML element where url can be found.

        Behavior :
            - Navigate to a specific HTML element where url of a specific product can be found.
            - Check if the href attribute that holds the url exist in the target HTML element.
            - fetch the URL from HTML tag.
        """
        try:
            url = 'Not Found'
            url_tag = tag.find('a',{'class':'reversed-link'})
            if url_tag and url_tag.has_attr('href'):
                url = url_tag['href']
                if not 'https:' in url:
                    url = f'https://urbangadgets.ph{url}'
            return url
        except Exception as e:
            print(f'[x] Unhandled exception while fetching url on rank-{self.rank}: {e}')
    
    def get_price(self, tag : BeautifulSoup) -> str | None:
        """
        Navigates to a specific HTML element where price can be found.

        Returns the price of a specific product.

        Args :
            tag (BeautifulSoup) : represents the group of HTML elements that holds data for a specific product.

        Attributes :
            price (str) : represents the price for a specific product.
            priceTag (BeautifulSoup) : the target HTML where price can be found.

        Behavior :
            - Navigate to a specific tag that holds the price.
            - fetch the price from HTML tag.
        """
        try:
            price : str = '0.00'
            price_tag = tag.find('span',{'class':'price'}) or tag.find('span', {'class':'f-price-item f-price-item--sale'})
            if price_tag:
                price = price_tag.text
            return price
        except Exception as e:
            print(f'[x] Unhandled exception while fetching price on rank-{self.rank}: {e}')
