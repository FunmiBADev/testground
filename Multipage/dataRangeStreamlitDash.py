import streamlit as st
import pandas as pd
from datetime import datetime

# Set the title of the Streamlit app
st.title("JRE Versions Dashboard")

# Function to load data from the CSV file
def load_data(file_name):
    return pd.read_csv(file_name)

# Load data from the CSV file
today = datetime.now().strftime('%Y-%m-%d')
csv_file_name = f"jre_counts_{today}.csv"
data = load_data(csv_file_name)

# Select platform tag
platform_tags = data['platform_tag_name'].unique()
platform_tag_filter = st.selectbox("Select Platform Tag", options=platform_tags)

# Select date range
start_date = st.date_input('Start Date', value=pd.to_datetime('2023-01-01'))
end_date = st.date_input('End Date', value=pd.to_datetime('today'))

# Filter data by platform tag and date range
filtered_df = data[(data['platform_tag_name'] == platform_tag_filter) & 
                   (data['date'] >= start_date.strftime('%Y-%m-%d')) & 
                   (data['date'] <= end_date.strftime('%Y-%m-%d'))]

# Calculate counts
green_jres_count = filtered_df['green_jres_count'].sum()
eol_jres_count = filtered_df['eol_jres_count'].sum()
env_var_count = filtered_df['env_var_cmd_count'].sum()

# Display counts
st.write(f"Green JREs: {green_jres_count}")
st.write(f"End-of-Life JREs: {eol_jres_count}")
st.write(f"Environment Variables Count: {env_var_count}")

# Create a bar chart
chart_data = pd.DataFrame({
    'JRE Type': ['Green JREs', 'End-of-Life JREs', 'Environment Variables'],
    'Count': [green_jres_count, eol_jres_count, env_var_count]
})

st.bar_chart(chart_data.set_index('JRE Type'))
