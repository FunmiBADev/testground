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

    # Filter the DataFrame
    filtered_df = jre_df[jre_df['platform_tag'] == platform_tag_filter]

    # Aggregate counts
    green_jres_count = filtered_df['green_jres'].notna().sum()
    eol_jres_count = filtered_df['eol_jres'].notna().sum()
    env_var_count = filtered_df['env_var_count'].sum()

    # Display counts
    st.write(f"Green JREs: {green_jres_count}")
    st.write(f"End-of-Life JREs: {eol_jres_count}")
    st.write(f"Environment Variables Count: {env_var_count}")

    # Create a bar chart for display
    data = {
        'JRE Type': ['Green JREs', 'End-of-Life JREs', 'Environment Variables'],
        'Count': [green_jres_count, eol_jres_count, env_var_count]
    }
    bar_chart_df = pd.DataFrame(data)
    st.bar_chart(bar_chart_df)

# Call this function in the main app
display_aggregated_dashboard()
