from airflow import DAG
import os
from airflow.operators.python_operator import PythonOperator
from datetime import datetime, timedelta
import pandas as pd
from sqlalchemy import create_engine

def load_csv_to_db():
    # Database connection
    print("################# The Directory is: ", os.getcwd(), " hello hello")
    # self.connection_url = f"postgresql+psycopg2://{self.username}:{self.password}@{self.host}:{self.port}/{self.database}"
    # engine = create_engine('postgresql+psycopg2://postgres:hello@localhost:5434/traffic_data')
    # # Paths to CSV files
    # track_data_path = '../data/automobile_track.csv'
    # trajectory_data_path = '../data/automobile_trajectory.csv'

    # # Load data into DataFrame
    # track_data = pd.read_csv(track_data_path)
    # trajectory_data = pd.read_csv(trajectory_data_path)

    # # Load data into PostgreSQL
    # track_data.to_sql('track_data', con=engine, if_exists='replace', index=False)
    # trajectory_data.to_sql('trajectory_data', con=engine, if_exists='replace', index=False)

    # print("Data loaded successfully into PostgreSQL")

# Define the DAG
dag = DAG(
    'load_automobile_data',
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
load_data_task = PythonOperator(
    task_id='load_data_to_db',
    python_callable=load_csv_to_db,
    dag=dag,
)