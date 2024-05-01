from airflow import DAG
import os
from airflow.operators.python_operator import PythonOperator
from datetime import datetime, timedelta
import pandas as pd
from sqlalchemy import create_engine

print("THE CURRENT DIRECTORY IS",os.getcwd())  

from utils.data_cleaner import DataExtractor

extractor = DataExtractor(file_name='20181024_d1_0830_0900.csv')

def extract_data():

    df_track, df_trajectory = extractor.extract_clean_data()
    
    print(f"EXTRACTION : DONE EXTRACTING AND CLEANING DATA\nTRACKS: {df_track.shape} : TRAJECTORIES: {df_trajectory.shape}")

def save_to_csv():

    track_file_name, trajectory_file_name = extractor.save_to_csv()

    print(f"Data loaded to {track_file_name} and {trajectory_file_name}")

# Define the DAG
dag = DAG(
    'load_traffic_data',
    default_args={
        'owner': 'airflow',
        'depends_on_past': False,
        'start_date': datetime(year=2024, month=4, day=30),
        'email_on_failure': False,
        'email_on_retry': False,
        'retries': 1,
        'retry_delay': timedelta(minutes=5),
    },
    description='Load automobile data into PostgreSQL',
    schedule_interval=timedelta(seconds=60 * 60),
    dagrun_timeout=timedelta(seconds=60),
)

# Define the task
extract_data_task = PythonOperator(
    task_id='extract_data_from_raw_csv',
    python_callable=extract_data,
    dag=dag,
)
# Define the task
save_to_csv_task = PythonOperator(
    task_id='save_data_extracted_to_csv',
    python_callable=save_to_csv,
    dag=dag,
)

# Define the pipeline 
extract_data_task >> save_to_csv_task