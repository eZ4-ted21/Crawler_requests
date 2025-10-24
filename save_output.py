import csv
from access_gs import AccessGoogleSheet

class SaveOutput():
    """
    A class that represents saving Data into CSV and Googlesheets.
    TODO : save data to a postgressql database.

    Attributes :
        data (list of dict) : the list of scraped data.
        sheet (str) : the name or identifier of the google sheet where data should be uploaded

    Methods :
        saveToCSV() : the method that saves data to CSV.
        saveToGooglesheets() : the method that saves data to Googlesheet.
        TODO : method for saving data to Database.
    """

    def __init__(self, data : list[dict], sheet : str):
        """
        Initialize a new instance of the class with data and a target Google Sheet.

        Args:
            data (list of dict): A list of dictionaries representing the data to be written.
                                Each dictionary corresponds to a row, with keys as column headers.
            sheet (str): The name or identifier of the Google Sheet worksheet where the data should be uploaded.

        Attributes:
            data (list of dict): Stores the data provided during initialization.
            worksheet (AccessGoogleSheet): An instance used to interact with the specified Google Sheet worksheet for reading or writing data.
        """
        self.data = data
        self.worksheet = AccessGoogleSheet(sheet)

    def saveToCSV(self):
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
            print(f'[x] Unhandled exeption encountered on saving data to CSV : {e}.')
        print('Saved Data to CSV file.')

    def saveToGoogleSheet(self):
        """
        Upload data from a local CSV file ('output.csv') to a specified Google Sheet.

        Behavior:
            - Retrieves the specified worksheet using the AccessGoogleSheet instance.
            - Clears any existing data in the worksheet.
            - Reads data from 'output.csv' and uploads all rows to the worksheet.
            - Handles exceptions during the process and logs an error message if needed.
            - Prints a confirmation message upon successful upload.
        """
        try:
            newSheet = self.worksheet.getWorkSheet()
            newSheet.clear()
            with open('output.csv', 'r', newline='') as f:
                reader = csv.reader(f)
                rows = list(reader) 
                newSheet.update(rows) 
        except Exception as e:
            print(f'[x] Unhandled exeption encountered on saving data to Google Sheets : {e}.')
        print("CSV data uploaded to Google Sheet.")