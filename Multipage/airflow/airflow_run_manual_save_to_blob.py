# airflow_run_manual_save_to_blob.py

from jre_processor import JREProcessor
import logging

def run_manual_save_counts(swc_name):
    processor = JREProcessor()
    try:
        processor.manual_save_counts(swc_name)
        logging.info(f"Manual save counts successfully executed for {swc_name}.")
    except Exception as e:
        logging.error(f"Failed to execute manual save counts: {e}")
        raise
