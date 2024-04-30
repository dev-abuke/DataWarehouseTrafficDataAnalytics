from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python_operator import PythonOperator

# Define default and DAG-specific arguments
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2023, 1, 1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# Define the DAG
dag = DAG(
    'load_pneuma_data',
    default_args=default_args,
    description='Load pNEUMA dataset into PostgreSQL',
    schedule_interval=timedelta(days=1),
)

def load_data():
    # Your data loading logic here
    print("Data loaded successfully!")

# Define tasks
load_task = PythonOperator(
    task_id='load_pneuma_data',
    python_callable=load_data,
    dag=dag,
)

