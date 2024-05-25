To refactor the code into a multi-page Streamlit app with a sidebar, we will use Streamlit's st.sidebar and st.selectbox to navigate between pages. Here is the updated script:

1. Main Streamlit script (app.py):

This script sets up the sidebar and the navigation between the two tabs.

2. Individual tab scripts:

- aggregated_dashboard.py: Contains the code for the aggregated JRE Versions Dashboard.
- platform_dashboard.py: Contains the code for the platform-specific JRE Versions Dashboard.

3. Directory structure:
   Your directory structure should look like this:

your_script_directory/
├── configs/
│ ├── config.json
│ └── apis.json
├── pages/
│ ├── aggregated_dashboard.py
│ └── platform_dashboard.py
├── app.py
├── daily_counts.log
├── .env
└── requirements.txt

You can create the requirements.txt file manually, or if you already have a virtual environment set up
with the necessary packages, you can generate it with the following command:

pip freeze > requirements.txt
