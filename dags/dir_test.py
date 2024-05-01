from airflow.operators.python_operator import PythonOperator
from airflow import DAG
import os
import sys
from datetime import datetime, timedelta
import pandas as pd
from sqlalchemy import create_engine

print("THE CURRENT DIRECTORY IS",os.getcwd())  

sys.path.append(f'./utils')
sys.path.append(f'./data')
sys.path.insert(0,os.path.abspath(os.path.dirname(__file__)))

# os.chdir('./utils')

from utils.data_cleaner import DataExtractor

# extractor = DataExtractor(file_name='20181024_d1_0830_0900.csv')

def extract_data():

    print("This is From Dir test: The Working Directory is : ", os.getcwd())
    print("This is From Dur Test: The List of Directories is : ", os.listdir('./utils'))

def save_to_csv():
    print(f"Data is Saved to CSV")

# Define the DAG
dag = DAG(
    'directory_test',
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
    task_id='print_working_directory',
    python_callable=extract_data,
    dag=dag,
)
# Define the task
save_to_csv_task = PythonOperator(
    task_id='print_save_csv_directory',
    python_callable=save_to_csv,
    dag=dag,
)

# Define the pipeline 
extract_data_task >> save_to_csv_task