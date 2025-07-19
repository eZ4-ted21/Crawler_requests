import requests

class Downloader():

    def __init__(self):
        self.headers = None
        self.cookies = None

    def download(self, url):
        try:
            self.headers = self.get_headers()
            response = requests.get(url, headers=self.headers, cookies=self.cookies, timeout=10000)
            print(response.status_code)
            rawdata = response.text
            return rawdata
        except Exception as e:
            print('[x] Download Failure Exception')
    
    def get_headers(self):
        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'en-US,en;q=0.9',
            'Priority': 'u=0, i',
            'Referer': 'https://www.google.com/',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.5 Safari/605.1.15'
        }
        return headers

    def get_cookies(self):
        pass


