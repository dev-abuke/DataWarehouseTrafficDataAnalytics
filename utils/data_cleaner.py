import csv
from itertools import islice
import os
from logger import logger
import sys
class DataExtractor():
    
    def __init__(self, file_path: str)->None:
        try:
            print("Initialized data extractor object")
            self.file_path = file_path
            # self.logger=logger()
            # self.logger.info('Data extractor object Initialized')
        except:
            pass
    
    def get_columns_and_rows(self) -> tuple:
        """
        Reads the first 100 rows of a file

        Parameters:
            file_path (str): The path to the file

        Returns:
            tuple: A tuple containing the columns and rows of the file
        """
        try:
            with open(f'data/{self.file_path}', 'r', newline='') as f:
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
    
    def get_lines(self):
        with open(f"data/{self.file_path}", 'r', buffering=100000000) as file:
            return file.readlines()
