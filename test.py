
from ETL.get_clean_data import CleanData
from Parsers.ws_strat import Extract
from ETL.save_output import SaveOutput

# url = 'https://urbangadgets.ph/search?options%5Bprefix%5D=last&q=drones'
url = 'https://urbangadgets.ph/collections/all'
uuid = '378ef5ee-53c7-4612-b0e4-11c9621e0c6a'


if __name__ == '__main__':
    scraped_data = Extract(url).execute()
    print(scraped_data)
    sheet = 'Drones'
    data = CleanData(scraped_data)._getListData()
    SaveOutput(data).saveToCSV()
    SaveOutput(data).saveToGoogleSheet(sheet)
    # SaveOutput(data).saveToDB(uuid)
