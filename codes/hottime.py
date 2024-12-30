import sqlite3
import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
import altair as alt
import seaborn as sns
import matplotlib.pyplot as plt

# Database file paths
DB_PATH = r"E:\SIH FINAL\codes\real.db"
FEEDBACK_TABLE = 'Feedback'
QUEUE_TABLE = 'QUEUE_TABLE'
MAIL_RECORD_TABLE = 'mail_record'
Citizen_Central_Service_Record = "citizen_central_service_record"

# Helper function to load data from the database
def load_data(table_name):
    conn = sqlite3.connect(DB_PATH)
    query = f"SELECT * FROM {table_name};"
    data = pd.read_sql_query(query, conn)
    conn.close()
    return data

# Sidebar menu
st.sidebar.title("Navigation")
selected_table = st.sidebar.selectbox(
    "Choose a dashboard:",
    options=["Feedback", "Queue Data", "Mail Record","Citizen_Central_Service_Record"]
)

if selected_table == "Feedback":
    st.title("Feedback Dashboard")
    data = load_data(FEEDBACK_TABLE)

    if data.empty:
        st.error("The Feedback table is empty or unavailable.")
    else:
        st.subheader("Raw Data")
        st.write(data)

        # Bar Chart: Counter_No vs Service_Rating
        st.subheader("Bar Chart: Services vs Service_Rating")
        bar_chart = data.groupby('Counter_No')['Service_Rating'].mean().reset_index()
        bar_fig = px.bar(bar_chart, x='Counter_No', y='Service_Rating', title="Average Service Rating by Counter")
        st.plotly_chart(bar_fig)

        # Define a variable to track the best performing counter
        best_performance = None
        max_positive_count = 0

        for counter in ['Saving Bank', 'Mail']:
            st.subheader(f"Pie Chart: Sentiment for Counter_No = {counter}")
            counter_data = data[data['Counter_No'] == counter]
    
            if not counter_data.empty:
                sentiment_counts = counter_data['Sentiment'].value_counts().reset_index()
                sentiment_counts.columns = ['Sentiment', 'Count']
                pie_fig = px.pie(sentiment_counts, values='Count', names='Sentiment', 
                                title=f"Sentiment Distribution for {counter} Counter")
                st.plotly_chart(pie_fig)
        
                    # Check if "Positive" sentiment is present and update the best performance
                if 'Positive' in sentiment_counts['Sentiment'].values:
                    positive_count = sentiment_counts[sentiment_counts['Sentiment'] == 'Positive']['Count'].iloc[0]
                    if counter == 'Mail' and positive_count > max_positive_count:
                        best_performance = 'Mail Services'
                        max_positive_count = positive_count
            else:
                st.warning(f"No data available for Counter_No = {counter}.")
        
# Print top performance message if "Mail Services" has the highest positive sentiment
        if best_performance:
            st.success(f"Top Performance: {best_performance}")
        else:
            st.info("No top performance identified based on positive sentiment.")

elif selected_table == "Queue Data":
    st.title("Queue Monitoring Feeds Dashboard")
    data = load_data(QUEUE_TABLE)

    if data.empty:
        st.error("The Queue Data table is empty or unavailable.")
    else:
        # Rename columns for easier reference
        data.columns = ['Date', 'Time', 'Number_of_People', 'Difference_in_Count']
        data['Datetime'] = pd.to_datetime(data['Date'] + ' ' + data['Time'])

        st.subheader("Filter by Date")
        unique_dates = data['Date'].unique()
        selected_date = st.selectbox("Select a date to filter", options=unique_dates)
        filtered_data = data[data['Date'] == selected_date]

        if not filtered_data.empty:
            total_people_count = filtered_data['Number_of_People'].sum()
            st.metric(label=f"Total People Count on {selected_date}", value=int(total_people_count))

            st.subheader("Number of People in Queue Over Time")
            line_chart = alt.Chart(filtered_data).mark_line(point=True).encode(
                x=alt.X('Datetime:T', title='Time'),
                y=alt.Y('Number_of_People:Q', title='Number of People'),
                tooltip=['Datetime', 'Number_of_People']
            )
            st.altair_chart(line_chart)

            most_crowded_time = filtered_data.loc[filtered_data['Number_of_People'].idxmax(), 'Datetime']
            least_crowded_time = filtered_data.loc[filtered_data['Number_of_People'].idxmin(), 'Datetime']
            st.write(f"**Most crowded time:** {most_crowded_time}")
            st.write(f"**Least crowded time:** {least_crowded_time}")

            st.subheader("Heatmap of Difference in Queue Size Over Time")
            heatmap_data = filtered_data.pivot_table(
                index='Time', 
                columns='Date', 
                values='Difference_in_Count', 
                aggfunc='mean'
            )
            plt.figure(figsize=(10, 6))
            sns.heatmap(heatmap_data, annot=True, cmap="YlGnBu", cbar_kws={'label': 'Difference in Queue Count'})
            st.pyplot(plt)
        else:
            st.warning("No data available for the selected date.")

elif selected_table == "Mail Record":
    st.title("Mail Counter Service Dashboard")
    data = load_data(MAIL_RECORD_TABLE)

    if data.empty:
        st.error("The Mail Record table is empty or unavailable.")
    else:
        data['date'] = pd.to_datetime(data['date'])
        data['time_difference'] = pd.to_timedelta(data['time_difference'])

        date_filter = st.date_input("Select Date", value=datetime.now().date())
        location_filter = st.selectbox("Select Location", ["All"] + data['location'].unique().tolist())

        filtered_data = data[data['date'] == pd.to_datetime(date_filter)]
        if location_filter != "All":
            filtered_data = filtered_data[filtered_data['location'] == location_filter]

        if not filtered_data.empty:
            total_customers = len(filtered_data)
            avg_wait_time = filtered_data['time_difference'][filtered_data['time_difference'] > pd.Timedelta(0)].mean()
            avg_wait_time_str = str(avg_wait_time).replace("0 days ", "").split('.')[0]
            service_time_count = (filtered_data['time_difference'] == pd.Timedelta(minutes=2)).sum()

            st.metric("Total Customers", total_customers)
            st.metric("Average Waiting Time", avg_wait_time_str)
            st.metric("Service Time (Exactly 2 min)", service_time_count)

            st.subheader("Customer Waiting Time Analysis")
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

            st.subheader("Customer Performance Analysis")
            performance_counts = filtered_data['performance'].value_counts()
            performance_fig = px.pie(
                names=['Good (1)', 'Average (0)', 'Bad (-1)'],
                values=[performance_counts.get(1, 0), performance_counts.get(0, 0), performance_counts.get(-1, 0)],
                title="Performance Distribution",
            )
            st.plotly_chart(performance_fig)

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
            st.write("No data available for the selected filters.")

elif selected_table == "Citizen_Central_Service_Record":
    st.title("Citizen Central Service Record Dashboard")

    try:
        data = load_data(Citizen_Central_Service_Record)  # Ensure the table name matches exactly

        if data.empty:
            st.error("The Citizen Central Service Record table is empty or unavailable.")
        else:
            # Ensure correct column names
            data['date'] = pd.to_datetime(data['date'], errors='coerce')  # Convert date column to datetime
            if 'location' not in data.columns or 'service_type' not in data.columns:
                st.error("Required columns ('location', 'service_type') are missing in the dataset.")
            else:
                # Filters
                st.subheader("Filter Records")
                date_filter = st.date_input("Select Date", value=datetime.now().date())
                location_filter = st.selectbox("Select Location", ["All"] + data['location'].unique().tolist())

                # Apply filters
                filtered_data = data[data['date'] == pd.to_datetime(date_filter)]
                if location_filter != "All":
                    filtered_data = filtered_data[filtered_data['location'] == location_filter]

                if not filtered_data.empty:
                    # Service Type Distribution
                    st.subheader("Service Type Distribution")
                    service_fig = px.bar(
                        filtered_data,
                        x='service_type',
                        color='service_type',
                        title="Service Type Count",
                        labels={'service_type': 'Service Type', 'count': 'Count'},
                        color_discrete_sequence=px.colors.qualitative.Set2
                    )
                    service_fig.update_layout(title_font_size=20, legend_title="Service Type")
                    st.plotly_chart(service_fig)

                    # Location-wise Service Analysis
                    st.subheader("Location-wise Service Analysis")
                    location_fig = px.pie(
                        filtered_data,
                        names='location',
                        title="Service Distribution by Location",
                        color_discrete_sequence=px.colors.qualitative.Pastel
                    )
                    location_fig.update_layout(title_font_size=20)
                    st.plotly_chart(location_fig)

                    # Additional metrics or visualizations can be added here
                else:
                    st.warning("No data available for the selected filters.")
    except Exception as e:
        st.error(f"An error occurred while loading data: {str(e)}")
