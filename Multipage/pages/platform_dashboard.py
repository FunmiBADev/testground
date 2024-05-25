import streamlit as st
import pandas as pd

# Assuming combined_df is imported from app.py
from app import combined_df, platform_tags

st.title("Platform-Specific JRE Versions Dashboard")

platform_tag_filter = st.selectbox("Select Platform Tag", options=[tag['tag'] for tag in platform_tags])

filtered_df = combined_df[combined_df['platform_tag'] == platform_tag_filter]

st.write("## Green JREs")
green_jres_count = filtered_df['green_jres'].notna().sum()
st.write(f"Count: {green_jres_count}")
st.dataframe(filtered_df[filtered_df['green_jres'].notna()])

st.write("## End-of-Life JREs")
eol_jres_count = filtered_df['eol_jres'].notna().sum()
st.write(f"Count: {eol_jres_count}")
st.dataframe(filtered_df[filtered_df['eol_jres'].notna()])
