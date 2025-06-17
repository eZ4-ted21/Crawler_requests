from extract_strat import Extract
from model import Data


url = 'https://geeksforgeeks.org'
scraped_data = Extract().execute(url)
# print(scraped_data)


data = Data(
    title=scraped_data['title'],
    url=scraped_data['url']
    )

for item in data:
    print(item)