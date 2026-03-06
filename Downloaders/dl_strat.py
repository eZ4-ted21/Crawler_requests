import requests

class Downloader:
    """
    A class to represent a downloader.

    Methods:
        download(url) : the method for requesting HTML source for the given url.
        getHeaders() : the method that generates headers later to be used as parameters for requesting HTML source.
        getCookies() : the method that generates cookies later to be used as parameters for requesting HTML source.
    """

    def __init__(self):
        """
        Initialize a new instance of class with the url

        Args :
            url (str) : the url to be scraped
        """
        self.headers = None
        self.cookies = None

    def download(self, url : str) -> str | None:
        """
        Sends Requests using the given url and get the response

        Returns HTML source as rawData

        Attributes :
            response (Response) : the response from the executed requests
            rawdata (str) : the HTML source from the response

        Behavior :
            - calls getHeaders method
            - send requests for the given url
            - checks response status code
            - get response text if status code is 200
        """
        try:
            raw_data = None
            self.headers = self.get_headers()
            response = requests.get(url, headers=self.headers, cookies=self.cookies, timeout=10000)
            print(response.status_code)
            if response.status_code == 200:
                raw_data = response.text
            return raw_data
        except Exception as e:
            print(f'[x] Download Failure Exception{e}.')

    @staticmethod
    def get_headers() -> dict:
        """
        Generates headers

        Returns Headers

        Attributes :
            headers (dict) : the necessary headers later to be used as request parameters
        """
        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'en-US,en;q=0.9',
            'Priority': 'u=0, i',
            'Referer': 'https://www.google.com/',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (HTML, like Gecko) Version/18.5 Safari/605.1.15'
        }
        return headers

    @staticmethod
    def get_cookies():
        """
        TODO : Generate cookies
        """
        pass


