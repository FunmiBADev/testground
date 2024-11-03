# daily_jre_manual_save_to_blob.py

from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import logging
from airflow_run_manual_save_to_blob import run_manual_save_counts

# Set default arguments for the DAG
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
    'start_date': datetime(2024, 1, 1),  # Set to your preferred start date
}

# Define the DAG, which runs every day at 6 a.m.
with DAG(
    'daily_jre_manual_save_to_blob',
    default_args=default_args,
    description='Daily job to manually save JRE counts to Azure Blob Storage',
    schedule_interval='0 6 * * *',  # Cron schedule for 6 a.m. daily
    catchup=False,
) as dag:
    
    run_manual_save_task = PythonOperator(
        task_id='run_manual_save_counts_task',
        python_callable=run_manual_save_counts,
        op_args=['your_swc_name'],  # Replace 'your_swc_name' with the appropriate SWC name
        dag=dag,
    )
    
    run_manual_save_task
