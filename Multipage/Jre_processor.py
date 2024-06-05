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

    def get_password(self, platform_tag):
        """Return the appropriate password based on the platform tag."""
        return self.passuat if 'UAT' in platform_tag else self.password

    def get_platform_token(self, platform_endpoint, platform_tag):
        """Get platform token."""
        try:
            password = self.get_password(platform_tag)
            response = requests.post(f'{platform_endpoint}{self.PLATFORM_API_LOGIN}', auth=(self.username, password))
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
            platform_tag = stats["tag"]
            platform_tag_name = stats["tag_name"]

            platform_token = self.get_platform_token(platform_url, platform_tag)
            try:
                platform_defs = requests.get(f"{platform_url}{self.PLATFORM_API_PROCESS_DEFINITIONS}", headers={"Cookie": platform_token}).json()

                # Converting platform definitions to a DataFrame and enhancing it
                df = pd.DataFrame(data=platform_defs)
                df[['jre', 'env_var_count']] = df.apply(lambda row: self.find_jre(row['assemblies'], row['variables'], row['startCmd'] if row['startCmd'] else 'nocmd'), axis=1, result_type='expand')
                df = df[['name', 'host', 'jre', 'env_var_count']]

                df['jre_version'] = df['jre'].apply(self.parse_jre_version)

                # Add platform tag for filtering in Streamlit
                df['platform_tag'] = platform_tag

                all_data.append(df)

                logging.info(f'Successfully fetched and processed data from {platform_tag_name}')
            except Exception as e:
                logging.error(f'Error fetching data from {platform_tag_name}: {e}')

        self.combined_df = pd.concat(all_data).reset_index(drop=True)

        # Identify green_jres and eol_jres
        self.combined_df['green_jres'] = self.combined_df['jre_version'].apply(lambda x: x if x and (x.startswith('17') or x.startswith('21')) else None)
        self.combined_df['eol_jres'] = self.combined_df['jre_version'].apply(lambda x: x if x and x.startswith('1.8.0') and int(x.split('_')[1]) < 352 else None)

    def upload_to_azure(self, file_name, container_name, blob_name=None):
        """Upload a file to an Azure Blob Storage container."""
        if blob_name is None:
            blob_name = os.path.basename(file_name)
        
        blob_service_client = BlobServiceClient.from_connection_string(self.azure_connection_string)
        blob_client = blob_service_client.get_blob_client(container=container_name, blob=blob_name)
        
        try:
            with open(file_name, "rb") as data:
                blob_client.upload_blob(data, overwrite=True)
            logging.info(f"Successfully uploaded {file_name} to {container_name}/{blob_name}")
        except Exception as e:
            logging.error(f"Error uploading {file_name} to Azure Blob Storage: {e}")
            raise

    def save_daily_counts(self):
        today = datetime.now().strftime('%Y-%m-%d')
        data = []

        for tag in self.platform_tags:
            platform_tag_name = tag['tag_name']
            filtered_df = self.combined_df[self.combined_df['platform_tag'] == platform_tag_name]
            green_jres_count = filtered_df['green_jres'].notna().sum()
            eol_jres_count = filtered_df['eol_jres'].notna().sum()
            env_var_cmd_count = filtered_df['env_var_count'].notna().sum()

            data.append({
                'date': today,
                'platform_tag_name': platform_tag_name,
                'green_jres_count': green_jres_count,
                'eol_jres_count': eol_jres_count,
                'env_var_cmd_count': env_var_cmd_count
            })

        df = pd.DataFrame(data)
        csv_file_name = f"jre_counts_{today}.csv"
        df.to_csv(csv_file_name, index=False)

        self.upload_to_azure(csv_file_name, self.azure_container_name)

        logging.info(f"JRE Version for {today} saved and uploaded to Azure Blob Storage")

    def manual_save_counts(self):
        try:
            self.fetch_and_update_data()
            self.save_daily_counts()
        except Exception as e:
            logging.error(f"Manual save failed: {e}")
            raise
