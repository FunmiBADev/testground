import getpass
import requests
import pandas as pd
import streamlit as st
from datetime import datetime
import schedule
import threading
import time

# Credentials
username = 'testUser'
password = getpass.getpass(prompt="Enter your password: ")

# Platform Tags
platform_tags = [
    {'tag': 'AA42557', 'tag_name': 'PLATFORM', 'url': 'https://www.platform.com'},
    {'tag': 'AA34475', 'tag_name': 'PLATFORM_ONE', 'url': 'https://www.platformone.com'},
    {'tag': 'AA45492', 'tag_name': 'PLATFORM_TWO', 'url': 'https://www.platformtwo.com'}
]

# API Endpoints
PLATFORM_API_LOGIN = '/api/login'
PLATFORM_API_PROCESS_DEFINITIONS = '/api/proc/definitions'
PLATFORM_API_JRE = '/api/jre/display'

# Global variable to store combined DataFrame
combined_df = pd.DataFrame()

def get_platform_token(platform_endpoint, username, password):
    """Get platform token."""
    response = requests.post(f'{platform_endpoint}{PLATFORM_API_LOGIN}', auth=(username, password))
    for header in response.headers['Set-Cookie'].split(';'):
        if header.startswith('platform_token'):
            return header
    return ''

def find_jre(assemblies, variables, start_cmd):
    """Find Java Runtime Environment info."""
    jre_info = ''
    for assembly in assemblies:
        if 'jre' in assembly['name']:
            jre_info += f"ASSEMBLY = {assembly['name']}={assembly['version']}"
    for variable in variables:
        if 'JAVA_8' in variable['value']:
            jre_info += f"ENV_VARIABLE = {variable['value']}"
    if "JAVA_8" in start_cmd:
        jre_info += f"START_CMD = {start_cmd}"
    return jre_info

def parse_jre_version(jre_string):
    """Parse the JRE version from a string."""
    if 'ASSEMBLY =' in jre_string:
        return jre_string.split('=')[1]
    return None

def fetch_and_update_data():
    global combined_df
    all_data = []

    for stats in platform_tags:
        platform_url = stats["url"]
        platform_tag = stats["tag"]
        platform_tag_name = stats["tag_name"]

        platform_token = get_platform_token(platform_url, username, password)
        platform_defs = requests.get(f"{platform_url}{PLATFORM_API_PROCESS_DEFINITIONS}", headers={"Cookie": platform_token}).json()

        # Converting platform definitions to a DataFrame and enhancing it
        df = pd.DataFrame(data=platform_defs)
        df['jre'] = df.apply(lambda row: find_jre(row['assemblies'], row['variables'], row['startCmd'] if row['startCmd'] else 'nocmd'), axis=1)
        df = df[['name', 'host', 'jre']]

        df['jre_version'] = df['jre'].apply(parse_jre_version)

        # Add platform tag for filtering in Streamlit
        df['platform_tag'] = platform_tag

        all_data.append(df)

    combined_df = pd.concat(all_data).reset_index(drop=True)

    # Identify green_jres and eol_jres
    combined_df['green_jres'] = combined_df['jre_version'].apply(lambda x: x if x and (x.startswith('17') or x.startswith('21')) else None)
    combined_df['eol_jres'] = combined_df['jre_version'].apply(lambda x: x if x and x.startswith('1.8.0') and int(x.split('_')[1]) < 352 else None)

def scheduled_scan():
    while True:
        schedule.run_pending()
        time.sleep(1)

# Schedule the scan to run every 2 hours
schedule.every(2).hours.do(fetch_and_update_data)

# Start the scheduler in a new thread
scheduler_thread = threading.Thread(target=scheduled_scan)
scheduler_thread.daemon = True
scheduler_thread.start()

# Initial data fetch
fetch_and_update_data()

# Create Streamlit dashboard
st.title("JRE Versions Dashboard")

platform_tag_filter = st.selectbox("Select Platform Tag", options=[tag['tag'] for tag in platform_tags])

filtered_df = combined_df[combined_df['platform_tag'] == platform_tag_filter]

st.write("## Green JREs")
green_jres_count = filtered_df['green_jres'].notna().sum()
st.write(f"Count: {green_jres_count}")
st.dataframe(filtered_df[filtered_df['green_jres'].notna()])

st.write("## End-of-Life JREs")
eol_jres_count = filtered_df['eol_jres'].notna().sum()
st.write(f"Count: {eol_jres_count}")
st.dataframe(filtered_df[filtered_df['eol_jres'].notna()])



# In this updated code:

# The function parse_jre_version is added to extract the JRE version from the jre string.
# The DataFrame now includes jre_version, green_jres, and eol_jres columns.
# A Streamlit dashboard is created, allowing users to filter by platform_tag and view the counts and details of green_jres and eol_jres.
# To run the Streamlit dashboard, save the script as app.py and execute it using the Streamlit command:
streamlit run app.py

# Scheduling and Threading:

# Added the schedule library to schedule tasks.
# Defined fetch_and_update_data to fetch and update the data.
# Used schedule.every(2).hours.do(fetch_and_update_data) to schedule the function to run every 2 hours.
# Created a separate thread (scheduler_thread) to run the scheduler independently from the main Streamlit app.
# Streamlit Dashboard:

# Integrated the global DataFrame combined_df to be updated dynamically by the scheduled tasks.
# The Streamlit dashboard displays updated counts and details of green_jres and eol_jres based on the selected platform_tag.
# To run this setup, ensure you have the schedule and streamlit libraries installed:

pip install schedule streamlit
