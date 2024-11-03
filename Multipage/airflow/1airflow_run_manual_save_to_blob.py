# airflow_run_manual_save_to_blob.py

from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime
import os
from jre_processor import JREProcessor

# Define the default arguments for the DAG
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2024, 11, 1),  # You can set this to a specific start date
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# Define the DAG
with DAG('jre_manual_save_to_blob',
         default_args=default_args,
         schedule_interval='0 6 * * *',  # Every day at 6 AM
         catchup=False) as dag:

    def run_manual_save(swc_name='default_swc_name'):
        """Function to run the manual save."""
        processor = JREProcessor()
        processor.manual_save_counts(swc_name)

    # Create the Airflow task
    manual_save_task = PythonOperator(
        task_id='manual_save_counts_task',
        python_callable=run_manual_save,
        op_kwargs={'swc_name': 'your_specific_swc_name'}  # Replace with actual swc_name if needed
    )

    # Set the task dependencies (if any)
    manual_save_task
