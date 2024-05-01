import csv
from itertools import islice
import os
# from logger import logger
import sys
import pandas as pd
import os
class DataExtractor():
    
    def __init__(self, file_name: str)->None:
        try:
            # os.chdir("..")
            print("Initialized data extractor object")
            self.file_name = file_name
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
            with open(f'data/{self.file_name}', 'r', newline='') as f:
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
        with open(f"data/{self.file_name}", 'r', buffering=100000000) as file:
            return file.readlines()
    
    def extract_clean_data(self):
        
        lines = self.get_lines()

        lines_as_lists = [line.strip('\n').strip().strip(';').split(';') for line in lines]

        cols = lines_as_lists.pop(0)

        track_cols = cols[:4]

        trajectory_cols = ['track_id'] + cols[4:]
        
        track_info = []
        trajectory_info = []

        for row in lines_as_lists:
            track_id = row[0]

            # add the first 4 values to track_info
            track_info.append(row[:4]) 

            remaining_values = row[4:]
            # reshape the list into a matrix and add track_id
            trajectory_matrix = [ [track_id] + remaining_values[i:i+6] for i in range(0,len(remaining_values),6)]
            # add the matrix rows to trajectory_info
            trajectory_info = trajectory_info + trajectory_matrix

        self.df_track = pd.DataFrame(data=track_info, columns=track_cols)

        self.df_trajectory = pd.DataFrame(data=trajectory_info, columns=trajectory_cols)

        return self.df_track, self.df_trajectory
    def save_to_csv(self) -> tuple:
        track_file_name = 'automobile_track.csv'
        trajectory_file_name = 'automobile_trajectory.csv'
        
        self.df_track.to_csv(f'data/{track_file_name}', index=False)
        self.df_trajectory.to_csv(f'data/{trajectory_file_name}', index=False)
        
        return track_file_name, trajectory_file_name