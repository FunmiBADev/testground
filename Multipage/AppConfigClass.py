import streamlit as st
import pandas as pd
import os
import json
from datetime import datetime
from dotenv import load_dotenv
import requests
import logging

# Load environment variables from .env file
load_dotenv()

# Setup logging
logging.basicConfig(filename='daily_counts.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class Config:
    def __init__(self):
        self.platform_tags = [
            {"tag": "AA42557", "tag_name": "PLATFORM", "url": "https://www.platform.com"},
            {"tag": "AA34475", "tag_name": "PLATFORM_ONE", "url": "https://www.platformone.com"},
            {"tag": "AA45492", "tag_name": "PLATFORM_TWO", "url": "https://www.platformtwo.com"}
        ]
        self.apis = {
            "PLATFORM_API_LOGIN": "/api/login",
            "PLATFORM_API_PROCESS_DEFINITIONS": "/api/proc/definitions",
            "PLATFORM_API_JRE": "/api/jre/display"
        }

    def get_platform_tags(self):
        return self.platform_tags

    def get_apis(self):
        return self.apis

# Initialize config
config = Config()

# Load platform tags and API endpoints from Config class
platform_tags = config.get_platform_tags()
apis = config.get_apis()

# Credentials
username = 'testUser'

# API Endpoints
PLATFORM_API_LOGIN = apis['PLATFORM_API_LOGIN']
PLATFORM_API_PROCESS_DEFINITIONS = apis['PLATFORM_API_PROCESS_DEFINITIONS']
PLATFORM_API_JRE = apis['PLATFORM_API_JRE']

# Global variable to store combined DataFrame
combined_df = pd.DataFrame()

def get_password(platform_tag):
    if 'UAT' in [tag['tag'] for tag in platform_tags]:
        return os.getenv('PASSUAT')
    else:
        return os.getenv('PASSWORD')

def get_platform_token(platform_endpoint, username, platform_tag):
    """Get platform token."""
    try:
        password = get_password(platform_tag)
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
    for assembly in assemblies:
        if 'jre' in assembly['name']:
            jre_info += f"ASSEMBLY = {assembly['name']}={assembly['version']} "
    for variable in variables:
        if variable['value'] is not None and 'JAVA_8' in variable['value']:
            jre_info += f"ENV_VARIABLE = {variable['value']} "
    if "JAVA_8" in start_cmd :
        jre_info += f"START_CMD = {start_cmd}"
    return jre_info

def parse_jre_version(jre_string):
    """Parse the JRE version from a string."""
    if 'ASSEMBLY =' in jre_string:
        return jre_string.split('=')[-1]
    elif 'ENV_VARIABLE =' in jre_string:
        return jre_string.split('=')[-1]
    elif 'START_CMD =' in jre_string:
        return jre_string.split('=')[1]
    return None

def fetch_and_update_data():
    global combined_df
    all_data = []

    for stats in platform_tags:
        platform_url = stats["url"]
        platform_tag = stats["tag"]
        platform_password = get_password(platform_tag)

        platform_token = get_platform_token(platform_url, username, platform_password)
        try:
            platform_defs = requests.get(f"{platform_url}{PLATFORM_API_PROCESS_DEFINITIONS}", headers={"Cookie": platform_token}).json()

            # Converting platform definitions to a DataFrame and enhancing it
            df = pd.DataFrame(data=platform_defs)
            df[['jre', 'env_var_count']] = df.apply(lambda row: find_jre(row['assemblies'], row['variables'], row['startCmd'] if row['startCmd'] else 'nocmd'), axis=1, result_type='expand')
            df['jre_version'] = df['jre'].apply(parse_jre_version)
            df = df[['name', 'host', 'jre']]

            # Add platform tag for filtering in Streamlit
            df['platform_tag'] = platform_tag

            all_data.append(df)

            logging.info(f'Successfully fetched and processed data from {platform_tag_name}')
        except Exception as e:
            logging.error(f'Error fetching data from {platform_tag_name}: {e}')

    combined_df = pd.concat(all_data).reset_index(drop=True)

    # Identify green_jres and eol_jres
    combined_df['green_jres'] = combined_df['jre_version'].apply(lambda x: x if x and (x.startswith('17') or x.startswith('21') or x.startswith('1.8.0') and int(x.split('_')[1]) >= 352) else None)
    combined_df['eol_jres'] = combined_df['jre_version'].apply(lambda x: x if x and x.startswith('1.8.0') and int(x.split('_')[1]) < 352 else None)
    combined_df['env_var_cmd'] = combined_df['jre_version'].apply(lambda x: x if x and 'JAVA 8' in x else None)

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
