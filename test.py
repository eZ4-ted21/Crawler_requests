
import re
from extract_strat import Extract
from save_output import SaveOutput

url = 'https://urbangadgets.ph/category/aerial-photography/drone/?srsltid=AfmBOoq2ykFbvAeqBvZOAVZN9OA0nx_RoFbIeE_uoKCTS55CkxhBEHbf'

def _getRankData(page_key, rd_key, rank_data):
    try:
        rankData = {
            'PAGE' : re.sub(r'[^0-9.,]', '', page_key),
            'RANK': re.sub(r'[^0-9.,]', '', rd_key),
            'TITLE' : rank_data.get('price'),
            'URL' : rank_data.get('url'),
            'PRICE' : rank_data.get('price')
        }
    except Exception as e:
        print(f'x] Unhandled Exeption encountered while getting Data per Rank {e}')
    return rankData

def _getListData(scraped_data):
    try:
        data = []
        for page in scraped_data:
            page_key = list(page.keys())[0]
            page_data = page[page_key]
            for rd in page_data:
                rd_key = list(rd.keys())[0]
                rank_data = rd[rd_key]
                data.append(_getRankData(page_key, rd_key, rank_data))
    except Exception as e:
        print(f'[x] Unhandled Exeption encountered while getting list of Data {e}')
    return data

if __name__ == '__main__':
    scraped_data = Extract().execute(url)
    print(scraped_data)
    data = _getListData(scraped_data)
    SaveOutput().saveToCSV(data)
    SaveOutput().saveToGoogleSheet()