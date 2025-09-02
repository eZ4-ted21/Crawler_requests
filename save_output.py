import csv
import gspread
from google.oauth2.service_account import Credentials
from dotenv import load_dotenv
import os

class SaveOutput():
    def __init__(self):
        pass

    def saveToCSV(self, _data):
        try:
            with open('output.csv', 'w', newline='') as csvfile:
                fieldnames = _data[0].keys()
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                
                writer.writeheader()
                writer.writerows(_data)
        except Exception as e:
            print(f'[x] Unhandled exeption encountered on saving data to CSV : {e}')
        print('Saved Data to CSV file.')

    def saveToGoogleSheet(self):
        try: 
            gs_id = os.getenv("GS_ID")
            scopes = ["https://www.googleapis.com/auth/spreadsheets"]
            creds = Credentials.from_service_account_file("gs_creds.json", scopes=scopes)
            client = gspread.authorize(creds)
            sheet_id = gs_id
            workbook = client.open_by_key(sheet_id)
            sheet = workbook.worksheet('Drones')
            sheet.clear()
            with open('output.csv', 'r', newline='') as f:
                reader = csv.reader(f)
                rows = list(reader) 
                sheet.update(rows) 
        except Exception as e:
            print(f'[x] Unhandled exeption encountered on saving data to Google Sheets : {e}')
        print("CSV data uploaded to Google Sheet.")