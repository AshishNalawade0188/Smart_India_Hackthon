import streamlit as st
import sqlite3
from datetime import datetime, timedelta

# Database connection
conn = sqlite3.connect(r'E:\SIH FINAL\codes\real2.db')
c = conn.cursor()

# Creating necessary tables
c.execute('''
CREATE TABLE IF NOT EXISTS mail_record (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date TEXT NOT NULL,
    name TEXT NOT NULL,
    mobile_number TEXT NOT NULL,
    location TEXT NOT NULL,
    pincode TEXT NOT NULL, 
    start_time TEXT,
    out_time TEXT,
    time_difference TEXT,
    performance INTEGER
)
''')

c.execute('''
CREATE TABLE IF NOT EXISTS mail_count_record_location (
    date TEXT PRIMARY KEY,
    count_Narayngav INTEGER DEFAULT 0,
    count_Alefata INTEGER DEFAULT 0
    
)
''')
c.execute('''
CREATE TABLE IF NOT EXISTS central_citizen_service_record (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date TEXT NOT NULL,
    name TEXT NOT NULL,
    mobile_number TEXT NOT NULL,
    location TEXT NOT NULL,
    pincode TEXT NOT NULL, 
    start_time TEXT,
    out_time TEXT,
    time_difference TEXT,
    performance INTEGER
)
''')

c.execute('''
CREATE TABLE IF NOT EXISTS central_citizen_service_count_record_location (
    date TEXT PRIMARY KEY,
    count_Narayngav INTEGER DEFAULT 0,
    count_Alefata INTEGER DEFAULT 0
    
)
''')
conn.commit()

# Function to update count tables
def update_count_column(location, date):
    """Updates the count for a given location in the count_table.

    Args:
        location: The location to update the count for.
        date: The date of the entry.
    """

    cursor = conn.cursor()

    cursor.execute("SELECT * FROM mail_count_record_location WHERE date = ?", (date,))
    existing_record = cursor.fetchone()

    if existing_record:
        # Update the count for the specific location
        update_query = f"UPDATE mail_count_record_location SET count_{location} = count_{location} + 1 WHERE date = ?"
        cursor.execute(update_query, (date,))
    else:
        # Insert a new record for the current date
        insert_query = f"INSERT INTO mail_count_record_location (date, count_{location}) VALUES (?, 1)"
        cursor.execute(insert_query, (date,))

    conn.commit()
def update_count_column_citizen_centric_service(location, date):
    """Updates the count for a given location in the count_table.

    Args:
        location: The location to update the count for.
        date: The date of the entry.
    """

    cursor = conn.cursor()

    cursor.execute("SELECT * FROM central_citizen_service_count_record_location WHERE date = ?", (date,))
    existing_record = cursor.fetchone()

    if existing_record:
        # Update the count for the specific location
        update_query = f"UPDATE central_citizen_service_count_record_location SET count_{location} = count_{location} + 1 WHERE date = ?"
        cursor.execute(update_query, (date,))
    else:
        # Insert a new record for the current date
        insert_query = f"INSERT INTO central_citizen_service_count_record_location (date, count_{location}) VALUES (?, 1)"
        cursor.execute(insert_query, (date,))

    conn.commit()

# Streamlit App
st.title("Post Office Management System")
menu = st.sidebar.radio("Menu", ["About Us", "Services"])

if menu == "About Us":
    st.header("About Us")
    st.write("""
        Welcome to the Post Office Management System! 
        This system provides services like mail handling, savings bank, payment bank, insurance, and citizen central services. 
        Explore our services to make your transactions easier and faster!
    """)

elif menu == "Services":
    st.header("Services")
    services = ["Mail","Citizen Central Service"]
    service_selected = st.selectbox("Select a Service", services)

    if service_selected == "Mail":
        st.subheader("Mail Service Form")

        # Network issue toggle
        network_issue = st.radio("Network Issue", ["Off", "On"], index=0)
        if "start_time" not in st.session_state:
            st.session_state["start_time"] = None
        if "pause_time" not in st.session_state:
            st.session_state["pause_time"] = None
        if "network_paused" not in st.session_state:
            st.session_state["network_paused"] = False

        if st.button("Enter Mail Service"):
            st.session_state["start_time"] = datetime.now()
            st.session_state["pause_time"] = None
            st.session_state["network_paused"] = False
            st.info(f"Start Time: {st.session_state['start_time'].strftime('%I:%M:%S %p')}")

        if network_issue == "On":
            if not st.session_state["network_paused"]:
                st.session_state["pause_time"] = datetime.now()
                st.session_state["network_paused"] = True
                st.warning("Network Issue: Timer paused.")
            else:
                if st.session_state["network_paused"]:
                    pause_duration = datetime.now() - st.session_state["pause_time"]
                    st.session_state["start_time"] += pause_duration
                    st.session_state["network_paused"] = False

        date = st.date_input("Date", value=datetime.now().date())
        name = st.text_input("Name")
        mobile_number = st.text_input("Mobile Number")
        location = st.selectbox("Location", ["Narayngav", "Alefata", "manchar", "ghodegav"])
        pincode = st.text_input("Pincode")

        if st.button("Submit"):
            out_time = datetime.now()
            start_time = st.session_state.get("start_time", None)

            if start_time:
                time_difference = out_time - start_time
                time_difference_str = str(time_difference)

                diff_in_seconds = time_difference.total_seconds()
                average_time = 2 * 60  # 3 minutes in seconds
                performance = (
                    -1 if diff_in_seconds > average_time else
                    1 if diff_in_seconds < average_time else
                    0
                )
            else:
                time_difference_str = None
                performance = None

            c.execute('''INSERT INTO mail_record (date, name, mobile_number, location, pincode, 
                          start_time, out_time, time_difference, performance) 
                          VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)''', 
                          (date, name, mobile_number, location, pincode, 
                           start_time.strftime('%I:%M:%S %p') if start_time else None, 
                           out_time.strftime('%I:%M:%S %p'), time_difference_str, performance))

            update_count_column(location, str(date))
            conn.commit()
            st.success("Mail record added successfully!")
    if service_selected == "Citizen Central Service":
        st.subheader("Citizen Central Service Form")

        # Network issue toggle
        network_issue = st.radio("Network Issue", ["Off", "On"], index=0)
        if "start_time" not in st.session_state:
            st.session_state["start_time"] = None
        if "pause_time" not in st.session_state:
            st.session_state["pause_time"] = None
        if "network_paused" not in st.session_state:
            st.session_state["network_paused"] = False

        if st.button("Enter Citizen Central Service"):
            st.session_state["start_time"] = datetime.now()
            st.session_state["pause_time"] = None
            st.session_state["network_paused"] = False
            st.info(f"Start Time: {st.session_state['start_time'].strftime('%I:%M:%S %p')}")

        if network_issue == "On":
            if not st.session_state["network_paused"]:
                st.session_state["pause_time"] = datetime.now()
                st.session_state["network_paused"] = True
                st.warning("Network Issue: Timer paused.")
            else:
                if st.session_state["network_paused"]:
                    pause_duration = datetime.now() - st.session_state["pause_time"]
                    st.session_state["start_time"] += pause_duration
                    st.session_state["network_paused"] = False

        date = st.date_input("Date", value=datetime.now().date())
        name = st.text_input("Name")
        mobile_number = st.text_input("Mobile Number")
        location = st.selectbox("Location", ["Narayngav", "Alefata", "manchar", "ghodegav"])
        pincode = st.text_input("Pincode")

        if st.button("Submit"):
            out_time = datetime.now()
            start_time = st.session_state.get("start_time", None)

            if start_time:
                time_difference = out_time - start_time
                time_difference_str = str(time_difference)

                diff_in_seconds = time_difference.total_seconds()
                average_time = 2 * 60  # 3 minutes in seconds
                performance = (
                    -1 if diff_in_seconds > average_time else
                    1 if diff_in_seconds < average_time else
                    0
                )
            else:
                time_difference_str = None
                performance = None

            c.execute('''INSERT INTO central_citizen_service_record (date, name, mobile_number, location, pincode, 
                          start_time, out_time, time_difference, performance) 
                          VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)''', 
                          (date, name, mobile_number, location, pincode, 
                           start_time.strftime('%I:%M:%S %p') if start_time else None, 
                           out_time.strftime('%I:%M:%S %p'), time_difference_str, performance))

            update_count_column_citizen_centric_service(location, str(date))
            conn.commit()
            st.success("central_citizen_service record added successfully!")

conn.close()