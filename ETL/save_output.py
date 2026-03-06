import csv
from GoogleSheets.access_gs import AccessGoogleSheet
from DB.access_db import GetDBConnection

class SaveOutput:
    """
    A class that represents saving Data into CSV and Googlesheets.
    TODO : save data to a postgres database.

    Attributes :
        data (list of dict) : the list of scraped data.
        sheet (str) : the name or identifier of the google sheet where data should be uploaded

    Methods :
        saveToCSV() : the method that saves data to CSV.
        saveToGooglesheets() : the method that saves data to Google sheet.
        TODO : method for saving data to Database.
    """

    def __init__(self, data : list[dict]):
        """
        Initialize a new instance of the class with data and a target Google Sheet.

        Args:
            data (list of dict): A list of dictionaries representing the data to be written.
                                Each dictionary corresponds to a row, with keys as column headers.

        Attributes:
            data (list of dict): Stores the data provided during initialization.
            work_sheet (AccessGoogleSheet): An instance used to interact with the specified Google Sheet worksheet for reading or writing data.
        """
        self.data = data
        self.work_sheet = AccessGoogleSheet()
        self.dbConn = GetDBConnection()

    def save_to_csv(self):
        """
        Save the provided data to a CSV file named 'output.csv'.

        Behavior:
            - Writes a header row based on the keys of the first dictionary.
            - Handles any exception during the file writing process and logs the error.
            - Prints a confirmation message upon successful saving.
        """
        try:
            with open('output.csv', 'w', newline='') as csvfile:
                fieldnames = self.data[0].keys()
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(self.data)
        except Exception as e:
            print(f'[x] Unhandled exception encountered on saving data to CSV : {e}.')
        print('Saved Data to CSV file.')

    def save_to_google_sheet(self, sheet):
        """
        Upload data from a local CSV file ('output.csv') to a specified Google Sheet.

        Args :
            sheet (str): The name or identifier of the Google Sheet worksheet where the data should be uploaded.

        Behavior:
            - Retrieves the specified worksheet using the AccessGoogleSheet instance.
            - Clears any existing data in the worksheet.
            - Reads data from 'output.csv' and uploads all rows to the worksheet.
            - Handles exceptions during the process and logs an error message if needed.
            - Prints a confirmation message upon successful upload.
        """
        try:
            new_sheet = self.work_sheet.get_work_sheet(sheet)
            new_sheet.clear()
            with open('output.csv', 'r', newline='') as f:
                reader = csv.reader(f)
                rows = list(reader) 
                new_sheet.update(rows)
        except Exception as e:
            print(f'[x] Unhandled exception encountered on saving data to Google Sheets : {e}.')
        print("CSV data uploaded to Google Sheet.")


    def save_to_db(self, uuid : str):
        """
        Saves data to database.

        Args:
            uuid (str) : the unique identifier for the category url.

        Behavior :
            - Gets database connection
            - loops on the data list and save each data into the category_data.
            - closes database connection after saving data
        """
        try:
            conn = GetDBConnection().getConnection()
            cur = conn.cursor()

            # SQL insert query
            insert_query = """
                INSERT INTO category_data(page, rank, title, url, price, uuid)
                VALUES (%s, %s, %s, %s, %s, %s)
            """

            for dt in self.data:
                prd_data = (dt['PAGE'], dt['RANK'], dt['TITLE'], dt['URL'], dt['PRICE'], uuid)
                cur.execute(insert_query, prd_data)

            # # Commit changes
            conn.commit()
            cur.close()
            conn.close()
        except Exception as e:
            print(f'[x] Unhandled exception encountered on saving data to Database : {e}.')
        print("Successfully save data to database.")

    
