# jre_processor.py

import pandas as pd
import os
import json
from datetime import datetime
from dotenv import load_dotenv
import requests
import logging
from azure.storage.blob import BlobServiceClient

class JREProcessor:
    def __init__(self, configs_dir='configs/'):
        load_dotenv()
        self.username = 'testUser'
        self.password = os.getenv('PASSWORD')
        self.passuat = os.getenv('PASSUAT')
        self.azure_connection_string = os.getenv('AZURE_CONNECTION_STRING')
        self.azure_container_name = os.getenv('AZURE_CONTAINER_NAME')

        # Setup logging
        logging.basicConfig(filename='daily_counts.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

        # Load configurations
        with open(os.path.join(configs_dir, 'config.json')) as config_file:
            config = json.load(config_file)
        self.platform_tags = config['platform_tags']

        with open(os.path.join(configs_dir, 'apis.json')) as apis_file:
            apis = json.load(apis_file)
        self.PLATFORM_API_LOGIN = apis['PLATFORM_API_LOGIN']
        self.PLATFORM_API_PROCESS_DEFINITIONS = apis['PLATFORM_API_PROCESS_DEFINITIONS']
        self.PLATFORM_API_JRE = apis['PLATFORM_API_JRE']

        self.combined_df = pd.DataFrame()

    # ... (rest of your class code)

if __name__ == "__main__":
    # Optional: Testing code to run only when executing this file directly.
    processor = JREProcessor()
    processor.manual_save_counts(swc_name)
