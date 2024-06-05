import streamlit as st
import pandas as pd

def display_aggregated_dashboard(jre_processor):
    st.title("JRE Versions Dashboard")

    platform_tag_filter = st.selectbox("Select Platform Tag", options=[tag['tag'] for tag in jre_processor.platform_tags])

    filtered_df = jre_processor.combined_df[jre_processor.combined_df['platform_tag'] == platform_tag_filter]

    green_jres_count = filtered_df['green_jres'].notna().sum()
    eol_jres_count = filtered_df['eol_jres'].notna().sum()
    env_var_count = filtered_df['env_var_count'].sum()

    # Display counts
    st.write(f"Green JREs: {green_jres_count}")
    st.write(f"End-of-Life JREs: {eol_jres_count}")
    st.write(f"Environment Variables Count: {env_var_count}")

    # Create a bar chart
    data = {'JRE Type': ['Green JREs', 'End-of-Life JREs', 'Environment Variables'], 'Count': [green_jres_count, eol_jres_count, env_var_count]}
    bar_chart_df = pd.DataFrame(data)
    st.bar_chart(bar_chart_df)

# Call this function in the main app
