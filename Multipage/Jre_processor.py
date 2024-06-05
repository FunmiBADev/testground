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

    def get_platform_token(self, platform_endpoint):
        """Get platform token."""
        try:
            response = requests.post(f'{platform_endpoint}{self.PLATFORM_API_LOGIN}', auth=(self.username, self.password))
            for header in response.headers['Set-Cookie'].split(';'):
                if header.startswith('platform_token'):
                    logging.info(f'Successfully obtained platform token from {platform_endpoint}')
                    return header
            logging.warning(f'Platform token not found in response from {platform_endpoint}')
        except Exception as e:
            logging.error(f'Error obtaining platform token from {platform_endpoint}: {e}')
        return ''

    def find_jre(self, assemblies, variables, start_cmd):
        """Find Java Runtime Environment info and count environment variables."""
        jre_info = ''
        env_var_count = 0
        for assembly in assemblies:
            if 'jre' in assembly['name']:
                jre_info += f"ASSEMBLY = {assembly['name']}={assembly['version']} "
        for variable in variables:
            if 'JAVA_8' in variable['value'] or 'JAVA_11' in variable['value'] or 'JAVA_17' in variable['value']:
                jre_info += f"ENV_VARIABLE = {variable['value']} "
                env_var_count += 1
        if "JAVA_8" in start_cmd or "JAVA_11" in start_cmd or "JAVA_17" in start_cmd:
            jre_info += f"START_CMD = {start_cmd}"
        return jre_info.strip(), env_var_count

    def parse_jre_version(self, jre_string):
        """Parse the JRE version from a string."""
        version = None
        if 'ASSEMBLY =' in jre_string:
            version = jre_string.split('ASSEMBLY =')[-1].split(' ')[0].split('=')[1]
        elif 'ENV_VARIABLE =' in jre_string:
            version = jre_string.split('ENV_VARIABLE =')[-1].split(' ')[0]
        elif 'START_CMD =' in jre_string:
            version = jre_string.split('START_CMD =')[-1].split(' ')[0]
        return version

    def fetch_and_update_data(self):
        all_data = []

        for stats in self.platform_tags:
            platform_url = stats["url"]
            platf
