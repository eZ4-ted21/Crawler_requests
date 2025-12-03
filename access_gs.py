import gspread
from google.oauth2.service_account import Credentials
import os 

class AccessGoogleSheet():
    """
    A class that represents Google Sheets connection.

    Methods :
        getWorkbook() : Establish Google Sheets connection.
        getWorkSheet() : Gets Worksheet where the data should be uploaded.
    """
    
    def __init__(self):
        """
        Initialize a new instance of the class with sheet.
        """

    def getWorkBook(self) -> gspread.spreadsheet.Spreadsheet:
        """
        Establish a connection to a Google Sheets workbook using service account credentials.

        Returns:
            gspread.spreadsheet.Spreadsheet: An authorized Google Sheets workbook instance.

        Behavior:
            - Loads the Google Sheet ID from the environment variable `GS_ID`.
            - Authenticates using service account credentials from the file `gs_creds.json`.
            - Connects to the specified Google Sheet using its ID.
            - Returns the workbook object for further operations.
        """
        try:
            gs_id = os.getenv("GS_ID")
            scopes = ["https://www.googleapis.com/auth/spreadsheets"]
            creds = Credentials.from_service_account_file("gs_creds.json", scopes=scopes)
            client = gspread.authorize(creds)
            sheet_id = gs_id
            workbook = client.open_by_key(sheet_id)
        except Exception as e:
            print(f'[x] Exeption encountered while getting access to google Workbook : {e}')
        return workbook
    
    def getWorkSheet(self, sheet : str) -> gspread.worksheet.Worksheet:
        """
        Retrieve a specific worksheet from the connected Google Sheets workbook.

        Returns:
            gspread.worksheet.Worksheet: The worksheet object corresponding to the provided name.

        Behavior:
            - Calls `getWorkBook()` to obtain the Google Sheets workbook instance.
            - Retrieves the worksheet with the given name from the workbook.
            - Logs an error message if the worksheet cannot be accessed.
        """
        try: 
            workbook = self.getWorkBook()
            newSheet = workbook.worksheet(sheet)
        except Exception as e:
            print(f'[x] Exception ecncountered while getting access to worksheet : {e}')
        return newSheet