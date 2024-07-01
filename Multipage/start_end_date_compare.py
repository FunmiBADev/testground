import streamlit as st
import pandas as pd
import datetime as dt
import matplotlib.pyplot as plt

# Load data
csv_file_name = "all_jre_counts.csv"
df = pd.read_csv(csv_file_name)

# Convert 'date' column to datetime
df['date'] = pd.to_datetime(df['date'])

# Title
st.title("JRE Versions Dashboard")

# Platform tag filter
platform_tags = df['platform_tag'].unique()
platform_tag_filter = st.selectbox("Select Platform Tag", options=platform_tags)

# Date filters
start_date = st.date_input("Start Date", dt.date.today() - dt.timedelta(days=30))
end_date = st.date_input("End Date", dt.date.today())

# Filter data based on selected platform tag and date range
filtered_df = df[(df['platform_tag'] == platform_tag_filter) & 
                 (df['date'] >= pd.to_datetime(start_date)) & 
                 (df['date'] <= pd.to_datetime(end_date))]

# Aggregate data by date
start_date_data = filtered_df[filtered_df['date'] == pd.to_datetime(start_date)].sum()
end_date_data = filtered_df[filtered_df['date'] == pd.to_datetime(end_date)].sum()

# Prepare data for plotting
jre_types = ['green_jres_count', 'eol_jres_count', 'env_var_count']
start_counts = [start_date_data[jre] for jre in jre_types]
end_counts = [end_date_data[jre] for jre in jre_types]

# Create a DataFrame for plotting
plot_df = pd.DataFrame({
    'JRE Type': ['Green JREs', 'End-of-Life JREs', 'Environment Variables'],
    'Start Date Count': start_counts,
    'End Date Count': end_counts
})

# Plot the data
fig, ax = plt.subplots()
plot_df.plot(kind='bar', x='JRE Type', ax=ax, color=['blue', 'orange'])

# Customize plot
ax.set_ylabel('Count')
ax.set_title(f'JRE Counts for {platform_tag_filter} from {start_date} to {end_date}')
ax.legend(['Start Date', 'End Date'])

# Display plot in Streamlit
st.pyplot(fig)
