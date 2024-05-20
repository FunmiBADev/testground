import getpass
import requests
import pandas as pd
import streamlit as st
from datetime import datetime
import schedule
import threading
import time
import plotly.express as px

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
            jre_info += f"ASSEMBLY = {assembly['name']}={assembly['version']} "
    for variable in variables:
        if 'JAVA_8' in variable['value'] or 'JAVA_11' in variable['value'] or 'JAVA_17' in variable['value']:
            jre_info += f"ENV_VARIABLE = {variable['value']} "
    if "JAVA_8" in start_cmd or "JAVA_11" in start_cmd or "JAVA_17" in start_cmd:
        jre_info += f"START_CMD = {start_cmd}"
    return jre_info.strip()

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

green_jres_count = filtered_df['green_jres'].notna().sum()
eol_jres_count = filtered_df['eol_jres'].notna().sum()

# Display counts
st.write(f"Green JREs: {green_jres_count}")
st.write(f"End-of-Life JREs: {eol_jres_count}")

# Create a bar chart
data = {'JRE Type': ['Green JREs', 'End-of-Life JREs'], 'Count': [green_jres_count, eol_jres_count]}
bar_chart_df = pd.DataFrame(data)

fig = px.bar(bar_chart_df, x='JRE Type', y='Count', title='JRE Versions Distribution')

st.plotly_chart(fig)
