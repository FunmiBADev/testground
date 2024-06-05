import streamlit as st
from jre_processor import JREProcessor

# Initialize the JREProcessor
jre_processor = JREProcessor()

# Initial data fetch
try:
    jre_processor.fetch_and_update_data()
    logging.info('Initial data fetch completed successfully.')
except Exception as e:
    logging.error(f'Error during initial data fetch: {e}')

# Streamlit sidebar for navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Aggregated Dashboard", "Platform Dashboard"])

if page == "Aggregated Dashboard":
    from pages.aggregated_dashboard import display_aggregated_dashboard
    display_aggregated_dashboard(jre_processor)
elif page == "Platform Dashboard":
    from pages.platform_dashboard import display_platform_dashboard
    display_platform_dashboard(jre_processor)

# Button for manual save
if st.sidebar.button('Manual Save Counts'):
    try:
        jre_processor.manual_save_counts()
        st.success("Manual save completed successfully.")
    except Exception as e:
        st.error(f"Manual save failed: {e}")
