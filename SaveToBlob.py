import streamlit as st
import pandas as pd
import os
import json
from datetime import datetime
from dotenv import load_dotenv
import requests
import logging
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient

# Load environment variables from .env file
load_dotenv()

# Setup logging
logging.basicConfig(filename='daily_counts.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Define the path to the configs directory
configs_dir = 'configs/'

# Load platform tags from configs/config.json
with open(os.path.join(configs_dir, 'config.json')) as config_file:
    config = json.load(config_file)
platform_tags = config['platform_tags']

# Load API endpoints from configs/apis.json
with open(os.path.join(configs_dir, 'apis.json')) as apis_file:
    apis = json.load(apis_file)

# Credentials
username = 'testUser'
password = os.getenv('PASSWORD')
azure_connection_string = os.getenv('AZURE_CONNECTION_STRING')
azure_container_name = os.getenv('AZURE_CONTAINER_NAME')

# API Endpoints
PLATFORM_API_LOGIN = apis['PLATFORM_API_LOGIN']
PLATFORM_API_PROCESS_DEFINITIONS = apis['PLATFORM_API_PROCESS_DEFINITIONS']
PLATFORM_API_JRE = apis['PLATFORM_API_JRE']

# Global variable to store combined DataFrame
combined_df = pd.DataFrame()

def get_platform_token(platform_endpoint, username, password):
    """Get platform token."""
    try:
        response = requests.post(f'{platform_endpoint}{PLATFORM_API_LOGIN}', auth=(username, password))
        for header in response.headers['Set-Cookie'].split(';'):
            if header.startswith('platform_token'):
                logging.info(f'Successfully obtained platform token from {platform_endpoint}')
                return header
        logging.warning(f'Platform token not found in response from {platform_endpoint}')
    except Exception as e:
        logging.error(f'Error obtaining platform token from {platform_endpoint}: {e}')
    return ''

def find_jre(assemblies, variables, start_cmd):
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

def parse_jre_version(jre_string):
    """Parse the JRE version from a string."""
    version = None
    if 'ASSEMBLY =' in jre_string:
        version = jre_string.split('ASSEMBLY =')[-1].split(' ')[0].split('=')[1]
    elif 'ENV_VARIABLE =' in jre_string:
        version = jre_string.split('ENV_VARIABLE =')[-1].split(' ')[0]
    elif 'START_CMD =' in jre_string:
        version = jre_string.split('START_CMD =')[-1].split(' ')[0]
    return version

def fetch_and_update_data():
    global combined_df
    all_data = []

    for stats in platform_tags:
        platform_url = stats["url"]
        platform_tag = stats["tag"]
        platform_tag_name = stats["tag_name"]

        platform_token = get_platform_token(platform_url, username, password)
        try:
            platform_defs = requests.get(f"{platform_url}{PLATFORM_API_PROCESS_DEFINITIONS}", headers={"Cookie": platform_token}).json()

            # Converting platform definitions to a DataFrame and enhancing it
            df = pd.DataFrame(data=platform_defs)
            df[['jre', 'env_var_count']] = df.apply(lambda row: find_jre(row['assemblies'], row['variables'], row['startCmd'] if row['startCmd'] else 'nocmd'), axis=1, result_type='expand')
            df = df[['name', 'host', 'jre', 'env_var_count']]

            df['jre_version'] = df['jre'].apply(parse_jre_version)

            # Add platform tag for filtering in Streamlit
            df['platform_tag'] = platform_tag

            all_data.append(df)

            logging.info(f'Successfully fetched and processed data from {platform_tag_name}')
        except Exception as e:
            logging.error(f'Error fetching data from {platform_tag_name}: {e}')

    combined_df = pd.concat(all_data).reset_index(drop=True)

    # Identify green_jres and eol_jres
    combined_df['green_jres'] = combined_df['jre_version'].apply(lambda x: x if x and (x.startswith('17') or x.startswith('21')) else None)
    combined_df['eol_jres'] = combined_df['jre_version'].apply(lambda x: x if x and x.startswith('1.8.0') and int(x.split('_')[1]) < 352 else None)

def upload_to_azure(file_name, container_name, blob_name=None):
    """Upload a file to an Azure Blob Storage container."""
    if blob_name is None:
        blob_name = os.path.basename(file_name)
    
    blob_service_client = BlobServiceClient.from_connection_string(azure_connection_string)
    blob_client = blob_service_client.get_blob_client(container=container_name, blob=blob_name)
    
    try:
        with open(file_name, "rb") as data:
            blob_client.upload_blob(data, overwrite=True)
        logging.info(f"Successfully uploaded {file_name} to {container_name}/{blob_name}")
    except Exception as e:
        logging.error(f"Error uploading {file_name} to Azure Blob Storage: {e}")
        raise

def save_daily_counts():
    global combined_df
    today = datetime.now().strftime('%Y-%m-%d')
    data = []

    for tag in platform_tags:
        platform_tag_name = tag['tag_name']
        filtered_df = combined_df[combined_df['platform_tag'] == platform_tag_name]
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

    upload_to_azure(csv_file_name, azure_container_name)

    logging.info(f"JRE Version for {today} saved and uploaded to Azure Blob Storage")

def manual_save_counts():
    try:
        fetch_and_update_data()
        save_daily_counts()
        st.success("Manual save completed successfully.")
    except Exception as e:
        st.error(f"Manual save failed: {e}")
        logging.error(f"Manual save failed: {e}")

# Initial data fetch
try:
    fetch_and_update_data()
    logging.info('Initial data fetch completed successfully.')
except Exception as e:
    logging.error(f'Error during initial data fetch: {e}')

# Streamlit sidebar for navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Aggregated Dashboard", "Platform Dashboard"])

if page == "Aggregated Dashboard":
    import pages.aggregated_dashboard
elif page == "Platform Dashboard":
    import pages.platform_dashboard

# Button for manual save
if st.sidebar.button('Manual Save Counts'):
    manual_save_counts()
