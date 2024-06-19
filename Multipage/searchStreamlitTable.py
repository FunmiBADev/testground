import streamlit as st
import pandas as pd
import requests
import logging

# Mock functions to replace with actual implementations
def get_platform_token(platform_url, username, password):
    # This function should return the token for the platform API
    return "token"

# Dummy data for platform_tags, username, password
platform_tags = [
    {"url": "http://example.com/api", "tag": "example_tag", "tag_name": "Example Platform"}
]
username = "username"
password = "password"
PLATFORM_API_PROCESS_DEFINITIONS = "/process_definitions"

# Define the functions
def find_jre(assemblies, variables, start_cmd):
    """Find Java Runtime Environment info and count environment variables."""
    jre_info = ''
    for assembly in assemblies:
        if 'jre' in assembly['name']:
            jre_info += f"ASSEMBLY = {assembly['name']}={assembly['version']} "
    for variable in variables:
        if variable['value'] is not None and 'JAVA_8' in variable['value']:
            jre_info += f"ENV_VARIABLE = {variable['value']} "
    if "JAVA_8" in start_cmd:
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
    combined_df['green_jres'] = combined_df['jre_version'].apply(lambda x: x if x and (x.startswith('17') or x.startswith('21') or (x.startswith('1.8.0') and int(x.split('_')[1]) >= 352)) else None)
    combined_df['eol_jres'] = combined_df['jre_version'].apply(lambda x: x if x and x.startswith('1.8.0') and int(x.split('_')[1]) < 352 else None)
    combined_df['env_var_cmd'] = combined_df['jre_version'].apply(lambda x: x if x and 'JAVA_8' in x else None)
    
    return combined_df

# Fetch and update data
combined_df = fetch_and_update_data()

st.title("JRE Versions Dashboard")

platform_tag_filter = st.selectbox("Select Platform Tag", options=[tag['tag'] for tag in platform_tags])

filtered_df = combined_df[combined_df['platform_tag'] == platform_tag_filter]

# Add text input for filtering the dataframe
query = st.text_input("Filter dataframe")

if query:
    mask = filtered_df.applymap(lambda x: query.lower() in str(x).lower()).any(axis=1)
    filtered_df = filtered_df[mask]

st.write("## Green JREs")
green_jres_count = filtered_df['green_jres'].notna().sum()
st.write(f"Count: {green_jres_count}")
st.dataframe(filtered_df[filtered_df['green_jres'].notna()])

st.write("## End-of-Life JREs")
eol_jres_count = filtered_df['eol_jres'].notna().sum()
st.write(f"Count: {eol_jres_count}")
st.dataframe(filtered_df[filtered_df['eol_jres'].notna()])

st.write("## ENV_VAR_CMDs")
env_var_cmd_count = filtered_df['env_var_cmd'].notna().sum()
st.write(f"Count: {env_var_cmd_count}")
st.dataframe(filtered_df[filtered_df['env_var_cmd'].notna()])

# https://discuss.streamlit.io/t/filter-data-in-data-editor/52055
# https://blog.streamlit.io/auto-generate-a-dataframe-filtering-ui-in-streamlit-with-filter_dataframe/
