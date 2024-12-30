import streamlit as st
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

# Connect to the SQLite database
conn = sqlite3.connect(r'E:\SIH FINAL\codes\real.db')
cursor = conn.cursor()

# Fetch the data from the Feedback table
query = "SELECT * FROM Feedback"
df = pd.read_sql(query, conn)

# Check the column names
st.write(df.columns)  # This will help you verify the column names

# Ensure proper column names and data types
df['Date'] = pd.to_datetime(df['Date'])
df['Sentiment'] = df['Sentiment'].astype(str)

# Display the table in Streamlit
st.title('Feedback Analysis Dashboard')

# Sidebar for selecting the service
services = df['Service'].unique()  # Adjusted column name
selected_service = st.sidebar.selectbox('Select a service', services)

# Filter the data for the selected service
service_data = df[df['Service'] == selected_service]  # Adjusted column name

# Count the feedback categories (Positive, Negative, Neutral)
feedback_count = service_data['Sentiment'].value_counts()

# Display the feedback count in the app
st.subheader(f"Feedback Distribution for {selected_service}")
st.write(feedback_count)

# Visualize the data using a bar chart
fig, ax = plt.subplots()
feedback_count.plot(kind='bar', color=['green', 'red', 'gray'], ax=ax)
ax.set_title(f"Feedback Sentiments for {selected_service}")
ax.set_ylabel('Number of Feedbacks')
ax.set_xlabel('Sentiment')
st.pyplot(fig)

# Optionally, add a pie chart for better visualization
st.subheader(f"Sentiment Pie Chart for {selected_service}")
fig_pie, ax_pie = plt.subplots()
feedback_count.plot(kind='pie', autopct='%1.1f%%', ax=ax_pie, colors=['green', 'red', 'gray'])
ax_pie.set_ylabel('')  # Remove the y-label to make it cleaner
ax_pie.set_title(f"Feedback Sentiment Distribution for {selected_service}")
st.pyplot(fig_pie)

# Optionally, add a table to show detailed feedback
st.subheader(f"Detailed Feedback for {selected_service}")
st.dataframe(service_data[['Date', 'Name', 'Sentiment', 'Feedback D']])

# Close the database connection
conn.close()
