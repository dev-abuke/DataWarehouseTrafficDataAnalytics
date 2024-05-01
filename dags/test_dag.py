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

from utils.data_cleaner import DataExtractor
from utils.db_conn_loader import DatabaseLoader

extractor = DataExtractor(file_name='20181024_d1_0830_0900.csv')

def extract_data():

    df_track, df_trajectory = extractor.extract_clean_data()
    
    print(f"EXTRACTION : DONE EXTRACTING AND CLEANING DATA\nTRACKS: {df_track.shape} : TRAJECTORIES: {df_trajectory.shape}")

def save_to_csv(ti):

    track_file_name, trajectory_file_name = extractor.save_to_csv()

    print(f"Data loaded to {track_file_name} and {trajectory_file_name}")

    ti.xcom_push(key="track_file_name",value=track_file_name)
    ti.xcom_push(key="trajectory_file_name",value=trajectory_file_name)

def init_db_conn(ti):
    
    print("INITIALIZING DATABASE CONNECTION")

    loader = DatabaseLoader()

    loader.connect()

    print("DATABASE CONNECTION INITIALIZED")

    ti.xcom_push(key="db_loader_instance",value=loader)

def load_data_to_db(ti):

    print("LOADING DATA TO DATABASE")
    
    loader: DatabaseLoader = ti.xcom_pull(key="db_loader_instance",task_ids='initialize_db_connection')

    track_file_name = ti.xcom_pull(key="track_file_name",task_ids='save_data_extracted_to_csv')

    trajectory_file_name = ti.xcom_pull(key="trajectory_file_name",task_ids='save_data_extracted_to_csv')

    loader.load_data_to_table(df=pd.read_csv(f'data/{track_file_name}.csv'), table_name=f'{track_file_name}')

    loader.load_data_to_table(df=pd.read_csv(f'data/{trajectory_file_name}.csv'), table_name=f'{trajectory_file_name}')

    print("DATA LOADED TO DATABASE")

# Define the DAG
dag = DAG(
    'traffic_data_analytics_data_warehouse',
    default_args={
        'owner': 'airflow',
        'depends_on_past': False,
        'start_date': datetime(year=2024, month=4, day=30, hour=12, minute=0), #datetime(2024, 4, 30, 12, 0)
        'email_on_failure': False,
        'email_on_retry': False,
        'retries': 1,
        'retry_delay': timedelta(minutes=5),
    },
    description='Load automobile data into PostgreSQL',
    schedule_interval=timedelta(days=1), # No Schedule Run Only Once
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

# Define the task
initialize_db = PythonOperator(
    task_id='initialize_db_connection',
    python_callable=init_db_conn,
    dag=dag,
)

# Define the task
load_to_db = PythonOperator(
    task_id='load_data_to_db',
    python_callable=load_data_to_db,
    dag=dag,
)

# Define the pipeline 
extract_data_task >> save_to_csv_task >> initialize_db >> load_to_db