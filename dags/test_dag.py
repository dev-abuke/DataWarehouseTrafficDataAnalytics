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

loader = DatabaseLoader()

def extract_data(ti):

    df_track, df_trajectory, track_file_name, trajectory_file_name = extractor.extract_clean_data()
    
    print(f"EXTRACTION : DONE EXTRACTING AND CLEANING DATA\nTRACKS: {df_track.shape} : TRAJECTORIES: {df_trajectory.shape}")

    ti.xcom_push(key="track_file_name",value=track_file_name)
    ti.xcom_push(key="trajectory_file_name",value=trajectory_file_name)

    print(f"DATA PUSH and EXTRACTION COMPLETED FILENAME {track_file_name} and {trajectory_file_name}")

def load_track_data_to_db(ti):

    print("LOADING TRACK DATA TO DATABASE")

    track_file_name = ti.xcom_pull(key="track_file_name",task_ids='extract_data_from_raw_csv')

    loader.load_data_to_table(df=pd.read_csv(f'data/{track_file_name}.csv'), table_name='track_data')

    print("TRACK DATA LOADED TO DATABASE")


def load_trajectory_data_to_db(ti):

    print("LOADING TRAJECTORY DATA TO DATABASE")

    trajectory_file_name = ti.xcom_pull(key="trajectory_file_name",task_ids='extract_data_from_raw_csv')

    loader.load_data_to_table(df=pd.read_csv(f'data/{trajectory_file_name}.csv'), table_name='trajectory_data')

    print("TRAJECTORY DATA LOADED TO DATABASE")

def create_db_func():
    loader.create_db('traffic_data')

def clean_up(ti):
    print("STARTING TO CLEAN UP")

    trajectory_file_name = ti.xcom_pull(key="trajectory_file_name",task_ids='extract_data_from_raw_csv')
    track_file_name = ti.xcom_pull(key="track_file_name",task_ids='extract_data_from_raw_csv')

    os.remove(f'data/{track_file_name}')
    os.remove(f'data/{trajectory_file_name}')

# Define the DAG
dag = DAG(
    'traffic_data_analytics_data_warehouse',
    default_args={
        'owner': 'airflow',
        'depends_on_past': False,
        'start_date': datetime(year=2024, month=4, day=30, hour=12, minute=0), #datetime(2024, 4, 30, 12, 0)
        'email_on_failure': False,
        'email_on_retry': False,
        'retries': 2,
        'retry_delay': timedelta(minutes=5),
    },
    description='Load automobile data into PostgreSQL',
    schedule_interval=timedelta(days=1), # No Schedule Run Only Once
)

# Define the task
extract_data_task = PythonOperator(
    task_id='extract_data_from_raw_csv',
    python_callable=extract_data,
    dag=dag,
)

load_track_to_db = PythonOperator(
    task_id='load_track_data_to_db',
    python_callable=load_track_data_to_db,
    dag=dag,
)

load_trajectory_to_db = PythonOperator(
    task_id='load_trajectory_data_to_db',
    python_callable=load_trajectory_data_to_db,
    dag=dag,
)
    
create_db = PythonOperator(
    task_id='create_table',
    python_callable = create_db_func,
    dag=dag,
)

clean_up_data = PythonOperator(
    task_id='clean_up_data',
    python_callable = clean_up,
    dag=dag,
)

# Define the pipeline 
[extract_data_task, create_db] >> load_track_to_db >> load_trajectory_to_db >> clean_up_data