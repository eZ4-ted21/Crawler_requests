import re
from bs4 import BeautifulSoup
from dl_strat import Downloader
from model import Data


class Extract():

    def __init__(self):
        self.downloder = Downloader()
        self.rank = 1
        self.page = 1
        self.nextUrl = None

    def execute(self, url:str) -> dict:
        dataAllPage : list = []
        self.nextUrl = url

        while True:
            try:
                if not self.nextUrl:
                    break
                
                print(f'Requesting on page : {self.page}')
                rawData = self.downloder.download(url=self.nextUrl)
                if not rawData: 
                    break

                dataPerPage = self.getDataPerPage(rawData)
                if not dataPerPage: 
                    break

                dataAllPage.append({f'page {self.page}':dataPerPage})
                self.page+=1
            except Exception as e:
                print(f'[x] Download Failure excepteion : {e}')
        return dataAllPage
        
    def getNextUrl(self, soup):
        try:
            self.nextUrl = None
            tag = soup.find('a',{'class':'next page-number'})
            if tag and tag.has_attr('href'):
                self.nextUrl = tag['href']
        except Exception as e:
            print(f'[x] Error ecounterd while fetching next url from page : {self.page}')
        return self.nextUrl
        
    def getDataPerPage(self, rawData):
        soup = BeautifulSoup(rawData, 'html.parser')
        self.nextUrl = self.getNextUrl(soup)
        dataPerPage = []

        tags = soup.find_all("div",{'class':'product-small box'})
        
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
    
    def validateData(self, tag):
        data = Data(
                    title = self.getTitle(tag),
                    url = self.getUrl(tag),
                    price = self.getPrice(tag)
                )
        return data
    

    def getTitle(self, tag) -> str:
        try:
            title = 'Not Found'
            titleTag = tag.find('p',{'class':'name product-title woocommerce-loop-product__title'})
            if titleTag:
                title = titleTag.get_text().strip()
        except Exception as e:
            print(f'[x] Unhandled exception while fetching title on rank-{self.rank}: {e}')
        return title

    def getUrl(self, tag) -> str:
        try:
            url = 'Not Found'
            urlTag = tag.find('a',{'class':'woocommerce-LoopProduct-link woocommerce-loop-product__link'})
            if urlTag and urlTag.has_attr('href'):
                url = urlTag['href']
        except Exception as e:
            print(f'[x] Unhandled exception while fetching url on rank-{self.rank}: {e}')
        return url
    
    def getPrice(self, tag) ->str:
        try:
            price : str = '0.00'
            priceTag = tag.find('span',{'class':'price'})
            if priceTag:
                price = priceTag.text
        except Exception as e:
            print(f'[x] Unhandled exception while fetching price on rank-{self.rank}: {e}')
        return price