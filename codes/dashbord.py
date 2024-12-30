import os
import sqlite3
import pandas as pd
import streamlit as st
import plotly.express as px
from datetime import date

# Database file path
db_path = r'E:\SIH FINAL\codes\post.db'  # Ensure this path is correct

# Function to test file path validity
if os.path.exists(db_path):
    st.write(f"Database file found: {db_path}")
else:
    st.error(f"Database file not found: {db_path}")

# Fetch data function with error handling
def fetch_data(query, params=None):
    """Fetch data from the SQLite database."""
    try:
        conn = sqlite3.connect(db_path)
        if params:
            df = pd.read_sql_query(query, conn, params=params)
        else:
            df = pd.read_sql_query(query, conn)
        return df
    except sqlite3.OperationalError as e:
        st.error(f"SQLite error: {e}")
        return pd.DataFrame()  # Return an empty DataFrame if error occurs
    finally:
        try:
            conn.close()
        except:
            pass

# Function to fetch combined data
def get_combined_data(start_date, end_date):
    """Fetch combined transaction data for all locations within the date range."""
    query = """
        SELECT 'Alephata' AS location, date, count_opening_account, count_closing_account, count_transaction, total_amount
        FROM payment_bank_count_record_alefata
        WHERE date BETWEEN ? AND ?
        UNION ALL
        SELECT 'Narayangaon' AS location, date, count_opening_account, count_closing_account, count_transaction, total_amount
        FROM payment_bank_count_record_narayangav
        WHERE date BETWEEN ? AND ?
    """
    return fetch_data(query, params=(start_date, end_date, start_date, end_date))

# Function to fetch data for a specific location
def get_location_data(location, start_date, end_date):
    """Fetch transaction data for a specific location within the date range."""
    table_name = "payment_bank_count_record_alefata" if location == "Alephata" else "payment_bank_count_record_narayangav"
    query = f"""
        SELECT date, count_opening_account, count_closing_account, count_transaction, total_amount
        FROM {table_name}
        WHERE date BETWEEN ? AND ?
    """
    return fetch_data(query, params=(start_date, end_date))

# Streamlit App
st.title("Real-Time Payment Bank Count Dashboard")

# Sidebar for location filter
locations = ["All", "Alephata", "Narayangaon"]
selected_location = st.sidebar.selectbox("Select Location", locations)

# Date range filter
start_date = st.sidebar.date_input("Start Date", value=date(2023, 1, 1))  # Adjust default value as needed
end_date = st.sidebar.date_input("End Date", value=date.today())

if start_date > end_date:
    st.error("Start date cannot be after end date.")

# Fetch data based on location filter
if selected_location == "All":
    data = get_combined_data(start_date, end_date)
else:
    data = get_location_data(selected_location, start_date, end_date)

# Visualization and Metrics
if not data.empty:
    st.subheader(f"Transaction Data for {selected_location} ({start_date} to {end_date})")

    # Dashboard Metrics
    total_opening = data['count_opening_account'].sum()
    total_closing = data['count_closing_account'].sum()
    total_transactions = data['count_transaction'].sum()
    total_amount = data['total_amount'].sum()

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Opening Accounts", total_opening)
    col2.metric("Total Closing Accounts", total_closing)
    col3.metric("Total Transactions", total_transactions)
    col4.metric("Total Transaction Amount", f"₹{total_amount:,.2f}")

    # Horizontal stacked bar chart for daily service counts
    bar_chart_data = data.melt(
        id_vars="date",
        value_vars=["count_opening_account", "count_closing_account", "count_transaction"],
        var_name="Service Category",
        value_name="Number of Transactions"
    )

    fig1 = px.bar(
        bar_chart_data,
        x="Number of Transactions",
        y="date",
        color="Service Category",
        text="Number of Transactions",  # Display count inside the bar
        title=f"Daily Service Counts (Horizontal Stacked) for {selected_location}",
        barmode="stack",
        orientation="h",
        labels={
            "date": "Transaction Date",
            "Number of Transactions": "Number of Transactions",
            "Service Category": "Type of Service"
        },
        color_discrete_sequence=px.colors.qualitative.Set3  # Updated color palette for clarity
    )
    fig1.update_traces(textposition="inside")  # Ensure text appears inside bars
    st.plotly_chart(fig1, use_container_width=True)

    # Pie chart for transaction distribution
    transaction_totals = data[['count_opening_account', 'count_closing_account', 'count_transaction']].sum()
    pie_chart_data = pd.DataFrame({
        "Transaction Type": transaction_totals.index.map({
            'count_opening_account': 'Opening Accounts',
            'count_closing_account': 'Closing Accounts',
            'count_transaction': 'Transactions'
        }),
        "Count": transaction_totals.values
    })
    fig2 = px.pie(
        pie_chart_data,
        names="Transaction Type",
        values="Count",
        title=f"Transaction Distribution for {selected_location}",
        color_discrete_sequence=px.colors.qualitative.Pastel  # Updated pie chart color palette
    )
    fig2.update_traces(
        textinfo="label+value",  # Show label and count only
        textfont_size=14  # Adjust font size for better readability
    )
    st.plotly_chart(fig2, use_container_width=True)

else:
    st.warning(f"No data available for {selected_location} between {start_date} and {end_date}.")
