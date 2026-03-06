from typing import Any

import gspread
from google.oauth2.service_account import Credentials
import os

from gspread import Spreadsheet


class AccessGoogleSheet:
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
        pass

    @staticmethod
    def _get_workbook() -> Spreadsheet | None:
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
            creds = Credentials.from_service_account_file("./gs_creds.json", scopes=scopes)
            client = gspread.authorize(creds)
            sheet_id = gs_id
            workbook = client.open_by_key(sheet_id)
            return workbook
        except Exception as e:
            print(f'[x] Exception encountered while getting access to google Workbook : {e}')

    
    def get_work_sheet(self, sheet : str) -> Any | None:
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
            workbook = self._get_workbook()
            new_sheet = workbook.worksheet(sheet)
            return new_sheet
        except Exception as e:
            print(f'[x] Exception encountered while getting access to worksheet : {e}')
