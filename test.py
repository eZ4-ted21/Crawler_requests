
from get_clean_data import CleanData
from extract_strat import Extract
from save_output import SaveOutput

url = 'https://urbangadgets.ph/category/aerial-photography/drone/?srsltid=AfmBOoq2ykFbvAeqBvZOAVZN9OA0nx_RoFbIeE_uoKCTS55CkxhBEHbf'
uuid = '378ef5ee-53c7-4612-b0e4-11c9621e0c6a'

if __name__ == '__main__':
    scraped_data = Extract(url).execute()
    print(scraped_data)
    sheet = 'Drones'
    data = CleanData(scraped_data)._getListData()
    SaveOutput(data).saveToCSV()
    SaveOutput(data).saveToGoogleSheet(sheet)
    # SaveOutput(data).saveToDB(uuid)
