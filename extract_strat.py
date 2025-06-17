from bs4 import BeautifulSoup
from dl_strat import Downloader

class Extract():

    def __init__(self):
        self.downloder = Downloader()

    def execute(self, url:str):
        rawData = self.downloder.download(url=url)
        soup = BeautifulSoup(rawData, 'html.parser')
        title = self.getTitle(soup)
        return {'url':url , 'title':title}

    def getTitle(self, soup):
        tag = soup.select_one('div.HomePageSearchContainer_homePageSearchContainer_heading__DhWmd')
        if tag:
            return tag.get_text().strip()
        return "Title not Found"