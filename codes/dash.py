import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px
from datetime import datetime

# Database connection
DB_path = r"E:\SIH FINAL\codes\real.db"
conn = sqlite3.connect(DB_path)

# Load data into a DataFrame
def load_data():
    query = "SELECT date, location, time_difference, performance FROM mail_record"
    df = pd.read_sql_query(query, conn)
    df['date'] = pd.to_datetime(df['date'])
    df['time_difference'] = pd.to_timedelta(df['time_difference'])
    return df

# Load the data
data = load_data()

# Streamlit App
st.title("Mail Counter Service Dashboard")

# Filters
date_filter = st.date_input("Select Date", value=datetime.now().date())
location_filter = st.selectbox("Select Location", ["All"] + data['location'].unique().tolist())

# Apply filters
filtered_data = data[data['date'] == pd.to_datetime(date_filter)]
if location_filter != "All":
    filtered_data = filtered_data[filtered_data['location'] == location_filter]

# Metrics
if not filtered_data.empty:
    total_customers = len(filtered_data)

    # Proper Average Waiting Time calculation
    avg_wait_time = filtered_data['time_difference'][filtered_data['time_difference'] > pd.Timedelta(0)].mean()
    avg_wait_time_str = str(avg_wait_time).replace("0 days ", "").split('.')[0]  # Format as HH:MM:SS

    # Service Time (default to 2 minutes)
    service_time_count = (filtered_data['time_difference'] == pd.Timedelta(minutes=2)).sum()

    st.metric("Total Customers", total_customers)
    st.metric("Average Waiting Time", avg_wait_time_str)
    st.metric("Service Time (Exactly 2 min)", service_time_count)
else:
    st.write("No data available for the selected filters.")

# Visualization - Waiting Time Analysis
if not filtered_data.empty:
    st.subheader("Customer Waiting Time Analysis")

    # Customer Waiting Time Bar Chart
    bar_fig = px.bar(
        filtered_data,
        x='location',
        y='time_difference',
        color='location',
        title="Waiting Time by Location",
        labels={'time_difference': 'Waiting Time'},
        text='time_difference'
    )
    bar_fig.update_traces(texttemplate='%{text}', textposition='outside')
    st.plotly_chart(bar_fig)

    # Performance Pie Chart
    st.subheader("Customer Performance Analysis")
    performance_counts = filtered_data['performance'].value_counts()
    performance_fig = px.pie(
        names=['Good (1)', 'Average (0)', 'Bad (-1)'],
        values=[performance_counts.get(1, 0), performance_counts.get(0, 0), performance_counts.get(-1, 0)],
        title="Performance Distribution",
    )
    st.plotly_chart(performance_fig)

    # Employee Performance Bar Chart
    st.subheader("Employee Performance Analysis")
    performance_bar_fig = px.bar(
        filtered_data,
        x='location',
        y='performance',
        color='performance',
        title="Employee Performance by Location",
        labels={'performance': 'Performance Score'},
        text='performance'
    )
    performance_bar_fig.update_traces(texttemplate='%{text}', textposition='outside')
    st.plotly_chart(performance_bar_fig)
else:
    st.write("No visualizations available due to lack of data.")

# Close the database connection
conn.close()