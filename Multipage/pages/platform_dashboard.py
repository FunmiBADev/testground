import streamlit as st

def display_platform_dashboard(jre_processor):
    st.title("JRE Versions Dashboard")

    platform_tag_filter = st.selectbox("Select Platform Tag", options=[tag['tag'] for tag in jre_processor.platform_tags])

    filtered_df = jre_processor.combined_df[jre_processor.combined_df['platform_tag'] == platform_tag_filter]

    st.write("## Green JREs")
    green_jres_count = filtered_df['green_jres'].notna().sum()
    st.write(f"Count: {green_jres_count}")
    st.dataframe(filtered_df[filtered_df['green_jres'].notna()])

    st.write("## End-of-Life JREs")
    eol_jres_count = filtered_df['eol_jres'].notna().sum()
    st.write(f"Count: {eol_jres_count}")
    st.dataframe(filtered_df[filtered_df['eol_jres'].notna()])

# Call this function in the main app

import streamlit as st
import pandas as pd
from datetime import datetime
from connect_to_duckdb import ConnectToDuckDB

# Initialize the connection to DuckDB with Azure settings
storage_account = "DREAM_STORAGE_ACCOUNT"
container = "JreStatusFolder"
connection_string = "DefaultEndpointsProtocol=https;AccountName=DREAM_STORAGE_ACCOUNT;AccountKey=YOUR_ACCOUNT_KEY;EndpointSuffix=core.windows.net"
duckdb_connector = ConnectToDuckDB(storage_account, container, connection_string)

def display_aggregated_dashboard():
    st.title("JRE Versions Dashboard")

    # Date selection
    date_str = st.date_input("Select Date", value=datetime.today()).strftime("%Y-%m-%d")
    jre_df = duckdb_connector.get_daily_jre_by_date(date_str)

    if jre_df is None:
        st.warning("No data available for the selected date.")
        return

    # Platform tag filter based on retrieved data
    platform_tags = jre_df['platform_tag'].unique()
    platform_tag_filter = st.selectbox("Select Platform Tag", options=platform_tags)

    # Filter the DataFrame based on the selected platform tag
    filtered_df = jre_df[jre_df['platform_tag'] == platform_tag_filter]

    # Display Green JREs
    st.write("## Green JREs")
    green_jres_count = filtered_df['green_jres'].notna().sum()
    st.write(f"Count: {green_jres_count}")
    st.dataframe(filtered_df[filtered_df['green_jres'].notna()])

    # Display End-of-Life JREs
    st.write("## End-of-Life JREs")
    eol_jres_count = filtered_df['eol_jres'].notna().sum()
    st.write(f"Count: {eol_jres_count}")
    st.dataframe(filtered_df[filtered_df['eol_jres'].notna()])

# Call this function in the main app
display_aggregated_dashboard()
