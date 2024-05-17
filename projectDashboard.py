# Install Required Packages:
# Ensure you have the required packages installed. You can install them using pip if you don't have them already:

# pip install streamlit pandas openpyxl

# Create the Streamlit dashboard: Below is the complete code for a Streamlit app that reads the Excel file from the provided URL and displays a dashboard to track the project status.

import streamlit as st
import pandas as pd

# URL of the Excel file
url = 'https://1drv.ms/x/s!AoCogIdHEXVIgpc4aWUTtgtOJ5hC2w?e=KicvWb'

# Function to load the data
@st.cache_data
def load_data(url):
    df = pd.read_excel(url)
    return df

# Load the data
df = load_data(url)

# Dashboard Title
st.title('Project Status Dashboard')

# Display the data
st.header('Project Data')
st.dataframe(df)

# Display summary metrics
total_projects = df.shape[0]
resolved_projects = df[df['Status'] == True].shape[0]
not_resolved_projects = df[df['Status'] == False].shape[0]

st.subheader('Summary Metrics')
st.write(f'Total Projects: {total_projects}')
st.write(f'Resolved Projects: {resolved_projects}')
st.write(f'Not Resolved Projects: {not_resolved_projects}')

# Filtered views
st.subheader('Projects by Status')
status_filter = st.radio('Select Status:', ('All', 'Resolved', 'Not Resolved'))

if status_filter == 'Resolved':
    filtered_df = df[df['Status'] == True]
elif status_filter == 'Not Resolved':
    filtered_df = df[df['Status'] == False]
else:
    filtered_df = df

st.dataframe(filtered_df)

# Provide links to project reports
st.subheader('Project Report Links')
for index, row in filtered_df.iterrows():
    st.markdown(f"[{row['Project']}]({row['Report Link']})")

# Highlight stale projects
st.subheader('Stale Projects')
stale_projects = df[df['Stale'] == True]
if not stale_projects.empty:
    st.write(f"There are {stale_projects.shape[0]} stale projects.")
    st.dataframe(stale_projects)
else:
    st.write("There are no stale projects.")

# Run the app with: streamlit run script_name.py (replace script_name.py with the name of your script file)

# Explanation:
# Loading Data: The load_data function fetches the Excel file from the provided URL and loads it into a pandas DataFrame. Using @st.cache_data ensures that the data is cached and reloaded only when necessary.

# Dashboard Structure:

# Title: Sets the title of the dashboard.
# Display Data: Shows the entire DataFrame.
# Summary Metrics: Provides summary statistics like the total number of projects, the number of resolved projects, and the number of not resolved projects.
# Filtered Views: Allows the user to filter projects based on their status using a radio button.
# Project Report Links: Displays clickable links to project reports.
# Stale Projects: Highlights projects marked as stale.
# Running the App: Save the code in a Python script (e.g., project_dashboard.py) and run it using Streamlit:

# streamlit run project_dashboard.py
