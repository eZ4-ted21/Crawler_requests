import requests

class Downloader():

    def __init__(self):
        self.headers = None
        self.cookies = None

    def download(self, url):
        response = requests.get(url, headers=self.headers, cookies=self.cookies)
        rawdata = response.text
        return rawdata
    
    def get_headers(self):
        pass

    def get_cookies(self):
        pass


