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
