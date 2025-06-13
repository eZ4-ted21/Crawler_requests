from bs4 import BeautifulSoup
from model import Data

from dl_strat import Downloader


class Extract():

    def __init__(self):
        self.downloder = Downloader()
        self.title = Data().title

    def execute(self, url:str):
        rawdata = self.downloder.download(url)
        return self.scrape(rawdata)

    def scrape(self, rawData:str):
        soup = BeautifulSoup(rawData, 'html.parser')
        tag = soup.select_one('div.HomePageSearchContainer_homePageSearchContainer_heading__DhWmd')
        if tag:
            self.title = tag.get_text().strip()
        return self.title