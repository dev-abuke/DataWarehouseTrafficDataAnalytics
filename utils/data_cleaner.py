import csv
from itertools import islice
from logger import Logger
import sys
class DataExtractor():
    
    def __init__(self)->None:
        try:
            self.logger=Logger().get_app_logger()
            self.logger.info('Data extractor object Initialized')
        except:
            pass
    
    def get_columns_and_rows(self, file_path: str) -> tuple:
        """
        Reads the first 100 rows of a file

        Parameters:
            file_path (str): The path to the file

        Returns:
            tuple: A tuple containing the columns and rows of the file
        """
        try:
            with open(f'../data/{file_path}', 'r', newline='') as f:
                reader = csv.reader(f, delimiter=';')
                columns, rows = next(reader), list(islice(reader, 99))
            return columns, rows
        except Exception as e:
            # the try excepts here are for the airflow
            try:
                self.logger.error(f"Failed to read data: {e}")
            except:
                pass
            sys.exit(1)
    