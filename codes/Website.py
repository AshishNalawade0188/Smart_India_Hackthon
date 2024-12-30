import streamlit as st
import pandas as pd
import os
import sqlite3
from streamlit_option_menu import option_menu
import base64
import runpy
import threading
import subprocess
import csv
from datetime import datetime, timedelta


# Define database path
db_path = r"E:\SIH FINAL\codes\real.db"

# Function to create table in the SQLite database if it doesn't exist
def create_feedback_table():
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Create table if it doesn't exist
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Feedback (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                Date TEXT,
                Name TEXT,
                Counter_No TEXT,
                Service_Rating INTEGER,
                Feedback_Description TEXT,
                Sentiment TEXT
            )
        ''')
        conn.commit()
        conn.close()
    except Exception as e:
        st.error(f"An error occurred while creating the table: {str(e)}")

# Function to save feedback to the SQLite database
def save_feedback(name, feedback_desc, sentiment, counter_no, rating):
    try:
        # Establish connection to the database
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # Get the current date and time
        date_time = datetime.now().strftime("%d-%m-%Y %H:%M:%S")

        # Insert the feedback data into the table
        cursor.execute('''
            INSERT INTO Feedback (Date, Name, Counter_No, Service_Rating, Feedback_Description, Sentiment)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (date_time, name, counter_no, rating, feedback_desc, sentiment))

        # Commit and close the connection
        conn.commit()
        conn.close()

        st.success("Thank you for your feedback!")
    except Exception as e:
        st.error(f"An error occurred while saving the feedback: {str(e)}")

# Create the Feedback table when the app starts
create_feedback_table()

# Streamlit App Configuration
st.set_page_config(page_title="Demo India Post", layout="wide")

# Function to encode image to base64
def load_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode()

# Path to your local background image
background_image_path = r"E:\SIH FINAL\images\background.jpg"
background_image = load_image(background_image_path)

# Custom CSS for background image and other styles
st.markdown(f"""
    <style>
    body {{
        background-image: url('data:image/jpg;base64,{background_image}');
        background-size: cover;
        background-repeat: no-repeat;
        background-attachment: fixed;
        color: white;
    }}
    </style>
""", unsafe_allow_html=True)

# Header Section
st.markdown('<div style="text-align: center; font-size: 50px; color: white; background-color: #cc0000; padding: 20px; border-radius: 5px;">Welcome to Demo India Post Management System</div>', unsafe_allow_html=True)



# Initialize SQLite database
conn = sqlite3.connect(r'E:\SIH FINAL\codes\real.db')
c = conn.cursor()

c.execute('''
CREATE TABLE IF NOT EXISTS mail_record (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date TEXT NOT NULL,
    name TEXT NOT NULL,
    mobile_number TEXT NOT NULL,
    location TEXT NOT NULL,
    pincode TEXT NOT NULL,
    service_type TEXT NOT NULL,
    start_time TEXT,
    out_time TEXT,
    time_difference TEXT,
    performance INTEGER
)
''')
c.execute('''
CREATE TABLE IF NOT EXISTS mail_count_record_narayangav (
    date TEXT PRIMARY KEY,
    count_booking_FC INTEGER DEFAULT 0,
    count_booking_SP INTEGER DEFAULT 0,
    count_booking_Business_class INTEGER DEFAULT 0,
    count_booking_international INTEGER DEFAULT 0,
    count_delivered_FC INTEGER DEFAULT 0,
    count_delivered_SP INTEGER DEFAULT 0,
    count_delivered_business_class INTEGER DEFAULT 0,
    count_delivered_international INTEGER DEFAULT 0
)
''')
c.execute('''
CREATE TABLE IF NOT EXISTS mail_count_record_alefata (
    date TEXT PRIMARY KEY,
    count_booking_FC INTEGER DEFAULT 0,
    count_booking_SP INTEGER DEFAULT 0,
    count_booking_Business_class INTEGER DEFAULT 0,
    count_booking_international INTEGER DEFAULT 0,
    count_delivered_FC INTEGER DEFAULT 0,
    count_delivered_SP INTEGER DEFAULT 0,
    count_delivered_business_class INTEGER DEFAULT 0,
    count_delivered_international INTEGER DEFAULT 0
)
''')
c.execute('''
CREATE TABLE IF NOT EXISTS mail_count_record_mancher (
    date TEXT PRIMARY KEY,
    count_booking_FC INTEGER DEFAULT 0,
    count_booking_SP INTEGER DEFAULT 0,
    count_booking_Business_class INTEGER DEFAULT 0,
    count_booking_international INTEGER DEFAULT 0,
    count_delivered_FC INTEGER DEFAULT 0,
    count_delivered_SP INTEGER DEFAULT 0,
    count_delivered_business_class INTEGER DEFAULT 0,
    count_delivered_international INTEGER DEFAULT 0
)
''')
c.execute('''
CREATE TABLE IF NOT EXISTS mail_count_record_ghodegav (
    date TEXT PRIMARY KEY,
    count_booking_FC INTEGER DEFAULT 0,
    count_booking_SP INTEGER DEFAULT 0,
    count_booking_Business_class INTEGER DEFAULT 0,
    count_booking_international INTEGER DEFAULT 0,
    count_delivered_FC INTEGER DEFAULT 0,
    count_delivered_SP INTEGER DEFAULT 0,
    count_delivered_business_class INTEGER DEFAULT 0,
    count_delivered_international INTEGER DEFAULT 0
)
''')
c.execute('''
CREATE TABLE IF NOT EXISTS saving_bank_record (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date TEXT NOT NULL,
    name TEXT NOT NULL,
    mobile TEXT NOT NULL,
    email TEXT NOT NULL,
    location TEXT NOT NULL,
    pincode TEXT NOT NULL, 
    amount REAL NOT NULL,
    service_type TEXT NOT NULL
)
''')

c.execute('''
CREATE TABLE IF NOT EXISTS saving_bank_count_record_narayangav (
        date TEXT PRIMARY KEY,
        count_opening_account INTEGER DEFAULT 0,
        count_closing_account INTEGER DEFAULT 0,
        count_transaction INTEGER DEFAULT 0,
        total_amount REAL DEFAULT 0
)
''')

c.execute('''
CREATE TABLE IF NOT EXISTS saving_bank_count_record_alefata (
    date TEXT PRIMARY KEY,
    count_opening_account INTEGER DEFAULT 0,
    count_closing_account INTEGER DEFAULT 0,
    count_transaction INTEGER DEFAULT 0,
    total_amount REAL DEFAULT 0
)
''')
c.execute('''
CREATE TABLE IF NOT EXISTS saving_bank_count_record_manchar (
    date TEXT PRIMARY KEY,
    count_opening_account INTEGER DEFAULT 0,
    count_closing_account INTEGER DEFAULT 0,
    count_transaction INTEGER DEFAULT 0,
    total_amount REAL DEFAULT 0
)
''')
c.execute('''
CREATE TABLE IF NOT EXISTS saving_bank_count_record_ghodegav (
    date TEXT PRIMARY KEY,
    count_opening_account INTEGER DEFAULT 0,
    count_closing_account INTEGER DEFAULT 0,
    count_transaction INTEGER DEFAULT 0,
    total_amount REAL DEFAULT 0
)
''')
c.execute('''
CREATE TABLE IF NOT EXISTS payment_bank_record (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date TEXT NOT NULL,
    name TEXT NOT NULL,
    mobile TEXT NOT NULL,
    email TEXT NOT NULL,
    location TEXT NOT NULL,
    pincode TEXT NOT NULL,
    amount REAL NOT NULL,
    service_type TEXT NOT NULL
)
''')

c.execute('''
CREATE TABLE IF NOT EXISTS payment_bank_count_record_narayangav (
    date TEXT PRIMARY KEY,
    count_opening_account INTEGER DEFAULT 0,
    count_closing_account INTEGER DEFAULT 0,
    count_transaction INTEGER DEFAULT 0,
    total_amount REAL DEFAULT 0
)
''')

c.execute('''
CREATE TABLE IF NOT EXISTS payment_bank_count_record_alefata (
    date TEXT PRIMARY KEY,
    count_opening_account INTEGER DEFAULT 0,
    count_closing_account INTEGER DEFAULT 0,
    count_transaction INTEGER DEFAULT 0,
    total_amount REAL DEFAULT 0
)
''')
c.execute('''
CREATE TABLE IF NOT EXISTS payment_bank_count_record_manchar (
    date TEXT PRIMARY KEY,
    count_opening_account INTEGER DEFAULT 0,
    count_closing_account INTEGER DEFAULT 0,
    count_transaction INTEGER DEFAULT 0,
    total_amount REAL DEFAULT 0
)
''')
c.execute('''
CREATE TABLE IF NOT EXISTS payment_bank_count_record_ghodegav (
    date TEXT PRIMARY KEY,
    count_opening_account INTEGER DEFAULT 0,
    count_closing_account INTEGER DEFAULT 0,
    count_transaction INTEGER DEFAULT 0,
    total_amount REAL DEFAULT 0
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

c.execute('''
CREATE TABLE IF NOT EXISTS count_record_citizen_central_service_narayangav (
    date TEXT PRIMARY KEY,
    count_Aadhar INTEGER DEFAULT 0,
    count_Passport_Seva INTEGER DEFAULT 0
)
''')

c.execute('''
CREATE TABLE IF NOT EXISTS count_record_citizen_central_service_alefata (
    date TEXT PRIMARY KEY,
    count_Aadhar INTEGER DEFAULT 0,
    count_Passport_Seva INTEGER DEFAULT 0
)
''')
c.execute('''
CREATE TABLE IF NOT EXISTS count_record_citizen_central_service_manchar (
    date TEXT PRIMARY KEY,
    count_Aadhar INTEGER DEFAULT 0,
    count_Passport_Seva INTEGER DEFAULT 0
)
''')
c.execute('''
CREATE TABLE IF NOT EXISTS count_record_citizen_central_service_ghodegav (
    date TEXT PRIMARY KEY,
    count_Aadhar INTEGER DEFAULT 0,
    count_Passport_Seva INTEGER DEFAULT 0
)
''')

c.execute('''
CREATE TABLE IF NOT EXISTS insurance_record (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date TEXT NOT NULL,
    name TEXT NOT NULL,
    mobile_number TEXT NOT NULL,
    email TEXT NOT NULL,
    location TEXT NOT NULL,
    service_type TEXT NOT NULL
)
''')


c.execute('''
CREATE TABLE IF NOT EXISTS count_record_insurance_narayangav (
    date TEXT PRIMARY KEY,
    count_PLI_Proaccured_Female INTEGER DEFAULT 0,
    count_PLI_Proaccured_male INTEGER DEFAULT 0,
    count_PLI_Proaccured_others INTEGER DEFAULT 0,
    count_RPLI_Proaccured_Female INTEGER DEFAULT 0,
    count_RPLI_Proaccured_male INTEGER DEFAULT 0,
    count_RPLI_Proaccured_others INTEGER DEFAULT 0
)
''')

c.execute('''
CREATE TABLE IF NOT EXISTS count_record_insurance_alefata (
    date TEXT PRIMARY KEY,
    count_PLI_Proaccured_Female INTEGER DEFAULT 0,
    count_PLI_Proaccured_male INTEGER DEFAULT 0,
    count_PLI_Proaccured_others INTEGER DEFAULT 0,
    count_RPLI_Proaccured_Female INTEGER DEFAULT 0,
    count_RPLI_Proaccured_male INTEGER DEFAULT 0,
    count_RPLI_Proaccured_others INTEGER DEFAULT 0
)
''')
c.execute('''
CREATE TABLE IF NOT EXISTS count_record_insurance_manchar (
    date TEXT PRIMARY KEY,
    count_PLI_Proaccured_Female INTEGER DEFAULT 0,
    count_PLI_Proaccured_male INTEGER DEFAULT 0,
    count_PLI_Proaccured_others INTEGER DEFAULT 0,
    count_RPLI_Proaccured_Female INTEGER DEFAULT 0,
    count_RPLI_Proaccured_male INTEGER DEFAULT 0,
    count_RPLI_Proaccured_others INTEGER DEFAULT 0
)
''')
c.execute('''
CREATE TABLE IF NOT EXISTS count_record_insurance_ghodegav (
    date TEXT PRIMARY KEY,
    count_PLI_Proaccured_Female INTEGER DEFAULT 0,
    count_PLI_Proaccured_male INTEGER DEFAULT 0,
    count_PLI_Proaccured_others INTEGER DEFAULT 0,
    count_RPLI_Proaccured_Female INTEGER DEFAULT 0,
    count_RPLI_Proaccured_male INTEGER DEFAULT 0,
    count_RPLI_Proaccured_others INTEGER DEFAULT 0
)
''')
c.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    email TEXT NOT NULL,
    mobile TEXT NOT NULL
)
''')

conn.commit()

# Function to update count tables
def update_count_table(location, date, service_type):
    table_name = {
        "Narayangav": "mail_count_record_narayangav",
        "Alefata": "mail_count_record_alefata",
        "manchar": "mail_count_record_mancher",
        "ghodegav": "mail_count_record_ghodegav"
    }.get(location, None)

    if table_name:
        c.execute(f"INSERT OR IGNORE INTO {table_name} (date) VALUES (?)", (date,))
        column_name = f"count_{service_type.replace(' ', '_')}"
        c.execute(f"UPDATE {table_name} SET {column_name} = {column_name} + 1 WHERE date = ?", (date,))
        conn.commit()

def update_saving_bank_count_table(location, date, service_type, amount):
    try:
        # Ensure service_type is a string
        service_type = str(service_type)
        
        # Determine the table name based on location
        table_name = "saving_bank_count_record_narayangav" if location == "Narayangav" else "saving_bank_count_record_alefata"
        
        # Insert or ignore the date entry
        c.execute(f"INSERT OR IGNORE INTO {table_name} (date, total_amount) VALUES (?, 0)", (date,))
        
        # Replace spaces in service_type with underscores to form the column name
        column_name = f"count_{service_type.replace(' ', '_')}"
        
        # Update the count and total_amount for the specific service type
        c.execute(f"UPDATE {table_name} SET {column_name} = {column_name} + 1, total_amount = total_amount + ? WHERE date = ?", (amount, date))
        
        # Commit the changes
        conn.commit()
    except Exception as e:
        print(f"Error in update_saving_bank_count_table: {e}")

def update_payment_bank_count_table(location, date, service_type, amount):
    table_name = "payment_bank_count_record_narayangav" if location == "Narayangav" else "payment_bank_count_record_alefata"
    c.execute(f"INSERT OR IGNORE INTO {table_name} (date, total_amount) VALUES (?, 0)", (date,))
    column_name = f"count_{service_type.replace(' ', '_')}"
    c.execute(f"UPDATE {table_name} SET {column_name} = {column_name} + 1, total_amount = total_amount + ? WHERE date = ?", (amount, date))
    conn.commit()

def update_citizen_service_count_table(location, date, service_type):
    table_name = "count_record_citizen_central_service_narayangav" if location == "Narayangav" else "count_record_citizen_central_service_alefata"
    c.execute(f"INSERT OR IGNORE INTO {table_name} (date) VALUES (?)", (date,))
    column_name = f"count_{service_type.replace(' ', '_')}"
    c.execute(f"UPDATE {table_name} SET {column_name} = {column_name} + 1 WHERE date = ?", (date,))
    conn.commit()

def update_insurance_count_table(location, date, service_type):
    table_name = "count_record_insurance_narayangav" if location == "Narayangav" else "count_record_insurance_alefata"
    c.execute(f"INSERT OR IGNORE INTO {table_name} (date) VALUES (?)", (date,))
    column_name = f"count_{service_type.replace(' ', '_')}"
    c.execute(f"UPDATE {table_name} SET {column_name} = {column_name} + 1 WHERE date = ?", (date,))
    conn.commit()


# Function to create the database (if not already created)
def create_db():
    conn = sqlite3.connect(r"E:\SIH FINAL\codes\real.db")
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS bookings (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT,
                        contact_number TEXT,
                        age INTEGER,
                        slot_time TEXT,
                        person_type TEXT)''')
    conn.commit()
    conn.close()

# Function to insert booking into the database
def insert_booking(name, contact_number, age, slot_time, person_type):
    conn = sqlite3.connect(r"E:\SIH FINAL\codes\real.db")
    cursor = conn.cursor()
    cursor.execute('''INSERT INTO bookings (name, contact_number, age, slot_time, person_type)
                      VALUES (?, ?, ?, ?, ?)''', (name, contact_number, age, slot_time, person_type))
    conn.commit()
    conn.close()

# Function to get available slots
def get_available_slots():
    available_slots = []
    # Define fixed time slots
    slots = ["10:00 to 10:10", "10:10 to 10:20", "10:20 to 10:30", "10:30 to 10:40", "10:40 to 10:50", 
             "10:50 to 11:00", "11:00 to 11:10", "11:10 to 11:20", "11:20 to 11:30", "11:30 to 11:40", 
             "11:40 to 11:50", "11:50 to 12:00", "12:00 to 12:10", "12:10 to 12:20", "12:20 to 12:30",
             "12:30 to 12:40", "12:40 to 12:50", "12:50 to 1:00", "1:00 to 1:10", "1:10 to 1:20", 
             "1:20 to 1:30", "1:30 to 1:40", "1:40 to 1:50", "1:50 to 2:00", "2:00 to 2:10", 
             "2:10 to 2:20", "2:20 to 2:30", "2:30 to 2:40", "2:40 to 2:50", "2:50 to 3:00", 
             "3:00 to 3:10", "3:10 to 3:20", "3:20 to 3:30", "3:30 to 3:40", "3:40 to 3:50", 
             "3:50 to 4:00", "4:00 to 4:10", "4:10 to 4:20", "4:20 to 4:30", "4:30 to 4:40", 
             "4:40 to 4:50", "4:50 to 5:00"]

    conn = sqlite3.connect(r"E:\SIH FINAL\codes\real.db")
    cursor = conn.cursor()
    
    # Check for existing bookings and remove booked slots from available ones
    cursor.execute('SELECT slot_time FROM bookings')
    booked_slots = cursor.fetchall()
    booked_slots = [slot[0] for slot in booked_slots]
    
    # Only keep the slots that are not already booked
    available_slots = [slot for slot in slots if slot not in booked_slots]

    conn.close()
    
    return available_slots

# Function to check if a name or contact number already exists in the bookings
def is_name_or_contact_existing(name, contact_number):
    conn = sqlite3.connect(r"E:\SIH FINAL\codes\real.db")
    cursor = conn.cursor()
    cursor.execute('SELECT name, contact_number FROM bookings WHERE name = ? OR contact_number = ?', (name, contact_number))
    existing_entry = cursor.fetchone()
    conn.close()
    return existing_entry is not None

# Function to write booking to CSV file
def write_to_csv(name, contact_number, age, slot_time, person_type):
    file_path = r"E:\SIH FINAL\datasets\bookings.csv"
    # Check if file exists, create header if it doesn't
    file_exists = os.path.exists(file_path)
    
    with open(file_path, mode='a', newline='') as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(["Name", "Contact Number", "Age", "Slot Time", "Person Type"])  # Write header
        writer.writerow([name, contact_number, age, slot_time, person_type])





ACCESS_NUMBER = "12345"

# Session state management
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

if "signup_complete" not in st.session_state:
    st.session_state["signup_complete"] = False

# Login function
def login():
    st.subheader("Login")
    username = st.text_input("Username", placeholder="Enter your username")
    password = st.text_input("Password", type="password", placeholder="Enter your password")

    if st.button("Login"):
        c.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
        user = c.fetchone()
        if user:
            st.session_state["authenticated"] = True
            st.success("Login successful! You now have access to the services.")
        else:
            if not st.session_state["signup_complete"]:
                st.warning("Please sign up first.")
            else:
                st.error("Invalid username or password. Please try again.")

# Signup function
def signup():
    st.subheader("Sign Up")
    username = st.text_input("Set Username", placeholder="Create your username")
    password = st.text_input("Set Password", type="password", placeholder="Create your password")
    email = st.text_input("Email", placeholder="Enter your email")
    mobile = st.text_input("Mobile Number", placeholder="Enter your mobile number")

    if username and password and email and mobile:
        access_code = st.text_input("Access Number", placeholder="Enter the provided access code")

        if st.button("Sign Up"):
            if access_code == ACCESS_NUMBER:
                try:
                    c.execute('''
                        INSERT INTO users (username, password, email, mobile)
                        VALUES (?, ?, ?, ?)
                    ''', (username, password, email, mobile))
                    conn.commit()
                    st.session_state["signup_complete"] = True
                    st.success("Sign-up successful! You can now log in.")
                except sqlite3.IntegrityError:
                    st.error("Username already exists. Please log in instead.")
            else:
                st.error("Sign-up failed. Access code does not match.")
    else:
        st.warning("Please fill all the fields before entering the access number.")

# Navigation Bar
selected_page = option_menu(
    menu_title=None,
    options=["Home", "About Us", "Services", "Feedback", "Help Center", "Dashboard","Booking Slot","Login/Sign Up"],
    icons=["house", "info-circle", "gear", "chat", "question-circle", "bar-chart","Booking", "Login"],
    menu_icon="cast",
    default_index=0,
    orientation="horizontal",
    styles={
        "container": {"padding": "0!important", "background-color": "#cc0000"},
        "icon": {"color": "white", "font-size": "20px"},
        "nav-link": {"color": "white", "font-size": "20px", "text-align": "center"},
        "nav-link-selected": {"background-color": "#990000"},
    }
)


# Home Page
if selected_page == "Home":
    # Heading
    st.markdown('<h3 style="font-size:35px; text-align: center;">Home</h3>', unsafe_allow_html=True)
    
    # Main Banner Image (Ensure the file path is valid on your system)
    st.image(r"E:\SIH FINAL\images\home.jpg", use_container_width=True)
    
    # Services Section
    st.markdown("""
    <div style="display: flex; flex-wrap: wrap; gap: 20px; justify-content: center; margin-top: 20px;">
        <!-- Mail Services -->
        <div style="width: 18%; background-color: #f8d7da; border: 1px solid #f5c6cb; padding: 20px; text-align: center; border-radius: 10px;">
            <h4 style="font-size:30px; color: #721c24;">Mail Services</h4>
            <p style="font-size:20px; color: #721c24;">
                Seamlessly delivering letters, parcels, and documents across India and internationally, India Post ensures reliable and timely communication.
            </p>
        </div>
        <!-- Saving Bank Services -->
        <div style="width: 18%; background-color: #d4edda; border: 1px solid #c3e6cb; padding: 20px; text-align: center; border-radius: 10px;">
            <h4 style="font-size:30px; color: #155724;">Saving Bank Services</h4>
            <p style="font-size:20px; color: #155724;">
                India Post offers savings accounts, recurring deposits, fixed deposits, and other financial solutions through its Post Office Savings Bank (POSB).
            </p>
        </div>
        <!-- Insurance -->
        <div style="width: 18%; background-color: #d1ecf1; border: 1px solid #bee5eb; padding: 20px; text-align: center; border-radius: 10px;">
            <h4 style="font-size:30px; color: #0c5460;">Insurance</h4>
            <p style="font-size:20px; color: #0c5460;">
                Tailored postal life insurance (PLI) and rural postal life insurance (RPLI) schemes cater to individuals and communities with affordable coverage.
            </p>
        </div>
        <!-- Citizen-Centric Services -->
        <div style="width: 18%; background-color: #fff3cd; border: 1px solid #ffeeba; padding: 20px; text-align: center; border-radius: 10px;">
            <h4 style="font-size:30px; color: #856404;">Citizen-Centric Services</h4>
            <p style="font-size:20px; color: #856404;">
                India Post facilitates Aadhaar enrollment, passport applications, and other critical services for the public.
            </p>
        </div>
        <!-- Payment Bank Services -->
        <div style="width: 18%; background-color: #d6d8d9; border: 1px solid #c8cbcf; padding: 20px; text-align: center; border-radius: 10px;">
            <h4 style="font-size:30px; color: #383d41;">Payment Bank Services</h4>
            <p style="font-size:20px; color: #383d41;">
                Payment banks provide basic banking services like deposits, withdrawals, fund transfers, and payments, but do not offer loans or credit services.
            </p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.subheader("YouTube Video")
    st.video("https://youtu.be/zItSmOEFl_A?si=G71Y8zs4BTTDMjKZ")



# Streamlit display logic
elif selected_page == "About Us":
    st.markdown("<h2 style='text-align: center; font-size: 35px;'>About Us</h2>", unsafe_allow_html=True)

    # Main Description
    st.markdown("""
    <p style="font-size: 25px; font-family: 'Times New Roman', Times, serif; color: black; text-align: justify;">
    For more than 150 years, the Department of Posts (DoP) has been the backbone of the country’s communication and has played a crucial role in the country’s socio-economic development. It touches the lives of Indian citizens in many ways: delivering mails, accepting deposits under Small Savings Schemes, providing life insurance cover under Postal Life Insurance (PLI) and Rural Postal Life Insurance (RPLI), and providing retail services like bill collection, sale of forms, etc. The DoP also acts as an agent for the Government of India in disbursing other services for citizens such as Mahatma Gandhi National Rural Employment Guarantee Scheme (MGNREGS) wage disbursement and old age pension payments. With more than 1,55,000 post offices, the DoP has the most widely distributed postal network in the world.
    </p>
""", unsafe_allow_html=True)
    st.subheader("YouTube Video")
    st.video("https://www.youtube.com/watch?v=aRF0nmr0eI8")


    # Automatically open the link when the "About Us" page is accessed with updated font size and style
    st.markdown("""
    <a href="https://www.indiapost.gov.in/VAS/Pages/AboutUs/AboutUs.aspx" target="_blank" 
       style="font-size: 32px; font-family: 'Times New Roman', Times, serif; text-decoration: none; color: #b30000;">
        Click here to visit Key Sections
    </a>
    """, unsafe_allow_html=True)

elif selected_page == "Services":
    if st.session_state["authenticated"]:
        st.header("Services")
        services = ["Mail", "Saving Bank", "Payment Bank", "Citizen Central Service", "Insurance"]
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
            location = st.selectbox("Location", ["Narayangav", "Alefata", "manchar", "ghodegav"])
            pincode = st.text_input("Pincode")
            service_type = st.selectbox("Service Type", [
                "booking_FC", "booking_SP", "booking_Business_class", "booking_international",
                "delivered_FC", "delivered_SP", "delivered_business_class", "delivered_international"
            ])

            if st.button("Submit"):
                out_time = datetime.now()
                start_time = st.session_state.get("start_time", None)

                if start_time:
                    time_difference = out_time - start_time
                    time_difference_str = str(time_difference)

                    diff_in_seconds = time_difference.total_seconds()
                    average_time = 1 * 60  # 3 minutes in seconds
                    performance = (
                        -1 if diff_in_seconds > average_time else 
                        1 if diff_in_seconds < average_time else 
                        0
                    )
                else:
                    time_difference_str = None
                    performance = None

                c.execute('''INSERT INTO mail_record (date, name, mobile_number, location, pincode, service_type, start_time, out_time, time_difference, performance) 
                            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', 
                        (date, name, mobile_number, location, pincode, service_type, 
                        start_time.strftime('%I:%M:%S %p') if start_time else None, 
                        out_time.strftime('%I:%M:%S %p'), time_difference_str, performance))

                update_count_table(location, str(date), service_type)
                conn.commit()
                st.success("Mail record added successfully!")
            
            

        elif service_selected == "Saving Bank":
                st.subheader("Saving Bank Service Form")
                # Input fields
                date = st.date_input("Date", value=datetime.now().date())
                name = st.text_input("Name")
                mobile = st.text_input("Mobile Number")
                email = st.text_input("Email")
                location = st.selectbox("Location", ["Narayangav", "Alefata"])
                pincode = st.text_input("Pincode")
                service_type = st.selectbox("Service Type", ["opening account", "closing account", "transaction"])
                amount = st.number_input("Amount", min_value=0, step=10)

                if st.button("Submit"):
                    # Save entry in the saving bank record table
                    c.execute('''
                    INSERT INTO saving_bank_record (date, name, mobile,email,location, pincode, amount,service_type)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                    ''', (date, name, mobile,email,location, pincode,amount,service_type))
                    conn.commit()

                    # Update count and total amount in the respective count table
                    update_saving_bank_count_table(location, str(date),amount,service_type)

                    st.success("Entry saved successfully!")
        elif service_selected == "Payment Bank":
                st.subheader("Payment Bank Service Form")
                # Input fields
                date = st.date_input("Date", value=datetime.now().date())
                name = st.text_input("Name")
                mobile = st.text_input("Mobile Number")
                email = st.text_input("Email")
                location = st.selectbox("Location", ["Narayangav", "Alefata"])
                pincode = st.text_input("Pincode")
                service_type = st.selectbox("Service Type", ["opening account", "closing account", "transaction"])
                amount = st.number_input("Amount", min_value=0.0, step=0.1)

                if st.button("Submit"):
                    # Save entry in the saving bank record table
                    c.execute('''
                    INSERT INTO payment_bank_record (date, name, mobile,email,location, pincode,amount,service_type)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                    ''', (date, name, mobile,email,location, pincode, amount, service_type))
                    conn.commit()

                    # Update count and total amount in the respective count table
                    update_payment_bank_count_table(location, str(date), service_type, amount)

                    st.success("Entry saved successfully!")
        elif service_selected == "Citizen Central Service":
                st.subheader("Citizen Central Service Form")
                
                # Input fields
                date = st.date_input("Date", value=datetime.now().date())
                name = st.text_input("Name")
                mobile = st.text_input("Mobile Number")
                email = st.text_input("Email")
                location = st.selectbox("Location", ["Narayangav", "Alefata"])
                service_type = st.selectbox("Service Type", ["Aadhar", "Passport Seva"])

                if st.button("Submit"):
                    # Save entry in the citizen central service record table
                    c.execute('''
                    INSERT INTO citizen_central_service_record (date, name, mobile,email,location, service_type)
                    VALUES (?, ?, ?, ?, ?, ? )
                    ''', (date, name, mobile,email,location, service_type))
                    conn.commit()

                    # Update count in the respective count table
                    update_citizen_service_count_table(location, str(date), service_type)

                    st.success("Entry saved successfully!")
        elif service_selected == "Insurance":
                st.subheader("Insurance Service Form")
                
                # Input fields
                date = st.date_input("Date", value=datetime.now().date())
                name = st.text_input("Name")
                mobile_number = st.text_input("Mobile Number")
                email = st.text_input("Email")
                location = st.selectbox("Location", ["Narayangav", "Alefata"])
                service_type = st.selectbox("Service Type", [
                    "PLI_Proaccured_Female", 
                    "PLI_Proaccured_male", 
                    "PLI_Proaccured_others", 
                    "RPLI_Proaccured_Female", 
                    "RPLI_Proaccured_male", 
                    "RPLI_Proaccured_others"
                ])

                if st.button("Submit"):
                    # Save entry in the insurance service record table
                    c.execute('''
                    INSERT INTO insurance_record (date,name, mobile_number,email, location, service_type)
                    VALUES (?, ?, ?, ?, ?, ?)
                    ''', (date,name, mobile_number,email,location, service_type))
                    conn.commit()

                    # Update count in the respective count table
                    update_insurance_count_table(location, str(date), service_type)

                    st.success("Entry saved successfully!")

    else:
            # Message if user tries to access services without logging in
            st.warning("You must log in or sign up to see the services.")


# Feedback page content
elif selected_page == "Feedback":
    st.markdown("### Counter System Feedback")

    # Input for the user's name
    st.markdown("<p style='font-size: 20px;'>Your Name:</p>", unsafe_allow_html=True)
    name = st.text_input("")

    # Dropdown for counter no
    st.markdown("<p style='font-size: 20px;'>Counter No:</p>", unsafe_allow_html=True)
    st.markdown("""
    <style>
    div[data-baseweb="select"] {
        font-size: 20px;  /* Adjust the font size for the dropdown content */
    }
    </style>
    """, unsafe_allow_html=True)
    counter_no = st.selectbox("", ["Mail", "Saving Bank", "Citizen Centric Services", "Insurance"])

    # Dropdown for overall rating on counter service
    st.markdown("<p style='font-size: 20px;'>Offer Service Rating:</p>", unsafe_allow_html=True)
    rating = st.selectbox("", [0,1,2,3,4,5])

    # Text area for feedback description
    st.markdown("<p style='font-size: 20px;'>Your Feedback Description:</p>", unsafe_allow_html=True)
    feedback_desc = st.text_area("")

    # Dropdown for overall feedback sentiment
    st.markdown("<p style='font-size: 20px;'>Overall Feedback Sentiment:</p>", unsafe_allow_html=True)
    overall_sentiment = st.selectbox("", ["Positive", "Negative", "Neutral"])

    # Custom CSS for the submit button
    st.markdown("""
        <style>
        .css-18e3th9 {
            background-color: #b30000 !important;
            color: white !important;
            font-size: 16px !important;
            border-radius: 5px !important;
        }
        </style>
    """, unsafe_allow_html=True)

    # Display the Submit Feedback button
    if st.button("Submit Feedback"):
        if name and feedback_desc:
            # Save the feedback to the database
            save_feedback(name, feedback_desc, overall_sentiment, counter_no, rating)
        else:
            st.error("Please fill in all the fields before submitting.")

    # Add a link to the original feedback page
    st.markdown("<a href='https://www.indiapost.gov.in/VAS/Pages/CustomerFeedback.aspx' style='font-size: 30px;'>Original Post Office Service Feedback</a>", unsafe_allow_html=True)

elif selected_page == "Help Center":
    st.markdown("### Help Center")
    
    st.markdown("""
    <p style="font-size: 24px;">Need help? Contact us:</p>
    <ul style="font-size: 25px;">
        <li>Email: <a href="mailto:support@indiapostdemo.com">support@indiapostdemo.com</a></li>
        <li>Phone: +91 1800 266 6868</li>
    </ul>
""", unsafe_allow_html=True)
    # Add a 'Now' link at the end of the feedback section with font size 30px
    # Create a container for the buttons
    st.markdown("""
    <div style="display: flex; justify-content: center; gap: 20px; margin-top: 20px;">
        <!-- Call Us Section -->
        <div style="width: 25%; background-color: #c9d4f1; border: 1px solid #ddd; padding: 20px; text-align: center; border-radius: 10px; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);">
            <div style="font-size: 40px; color: #007BFF;">
                📞
            </div>
            <h4 style="font-size: 24px; color: #333; margin: 10px 0;">CALL US</h4>
            <p style="font-size: 18px; color: #555;">1800 266 6868</p>
        </div>
        <!-- Visit Us Section -->
        <div style="width: 25%; background-color: #c9d4f1; border: 1px solid #ddd; padding: 20px; text-align: center; border-radius: 10px; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);">
            <div style="font-size: 40px; color: #007BFF;">
                📍
            </div>
            <h4 style="font-size: 24px; color: #333; margin: 10px 0;">VISIT US</h4>
            <p style="font-size: 18px; color: #555;">
                Directorate of Postal Post Office Complex, <br>
                1st Floor New Delhi – 110021
            </p>
        </div>
        <!-- Mail Us Section -->
        <div style="width: 25%; background-color: #c9d4f1; border: 1px solid #ddd; padding: 20px; text-align: center; border-radius: 10px; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);">
            <div style="font-size: 40px; color: #007BFF;">
                ✉
            </div>
            <h4 style="font-size: 24px; color: #333; margin: 10px 0;">MAIL US</h4>
            <p style="font-size: 18px; color: #555;">support@demoindiapost.in</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Add clickable columns
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown("""
        <a href='https://www.indiapost.gov.in/MBE/Pages/Content/Addressing-Tips.aspx' 
        style='text-decoration: none;'>
        <div style='border: 1px solid #eaeaea; border-radius: 10px; 
                    padding: 10px; text-align: center; background-color: #ffe6e6;'>
            <img src='file:///C:/Users/shaik/Desktop/post%20office/images/Mail.jpg' alt='Addressing' style='border-radius: 50%; width: 100px; height: 100px;'>
            <h4 style='color: #b30000;'>Addressing Tips</h4>
            <p>Seamlessly delivering letters, parcels, and documents across India.</p>
        </div>
        </a>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <a href='https://www.indiapost.gov.in/MBE/Pages/Content/Packaging-Tips.aspx' 
            style='text-decoration: none;'>
            <div style='border: 1px solid #eaeaea; border-radius: 10px; 
                        padding: 10px; text-align: center; background-color: #e6ffe6;'>
                <img src='file:///C:/Users/shaik/Desktop/post%20office/images/Mail.jpg' alt='Packaging' style='border-radius: 50%; width: 100px; height: 100px;'>
                <h4 style='color: #008000;'>Packaging Tips</h4>
                <p>India Post offers savings accounts, fixed deposits, and more.</p>
            </div>
        </a>
    """, unsafe_allow_html=True)



    with col3:
        st.markdown("""
    <a href='https://www.indiapost.gov.in/VAS/Pages/Form.aspx' 
       style='text-decoration: none;'>
       <div style='border: 1px solid #eaeaea; border-radius: 10px; 
                   padding: 10px; text-align: center; background-color: #e6f7ff;'>
            <img src='file:///C:/Users/shaik/Desktop/post%20office/images/Mail.jpg' alt='Forms' style='border-radius: 50%; width: 100px; height: 100px;'>
            <h4 style='color: #004080;'>Forms</h4>
            <p>Tailored postal life insurance for individuals and communities.</p>
        </div>
    </a>
    """, unsafe_allow_html=True)

    with col4:
        st.markdown("""
    <a href='https://drive.google.com/drive/folders/1OvxLy4-4O4xjAN1Ga1Wm_edfbe8vkui0?usp=sharing' 
       style='text-decoration: none;'>
       <div style='border: 1px solid #eaeaea; border-radius: 10px; 
                   padding: 10px; text-align: center; background-color: #ffffe6;'>
            <img src='file:///C:/Users/shaik/Desktop/post%20office/images/Mail.jpg' alt='Reference' style='border-radius: 50%; width: 100px; height: 100px;'>
           <h4 style='color: #b38f00;'>Region Reference</h4>
           <p>Reference form slip for correcting forms.</p>
       </div>
    </a>
    """, unsafe_allow_html=True)

    
elif selected_page == "Dashboard":
    if st.session_state.get("authenticated", False):
        st.markdown("<h3>Welcome to the Dashboard</h3>", unsafe_allow_html=True)
        
        
        def run_streamlit_script(script_path):
            """Function to run a Streamlit script using subprocess."""
            try:
                subprocess.Popen(["streamlit", "run", script_path], shell=True)  # Non-blocking
                st.success(f"Dashboard {script_path} is launching...")
            except Exception as e:
                st.error(f"Failed to launch dashboard: {e}")

        # Button to launch the Streamlit dashboard
        if st.button("Open Dashboard"):
            script_path = r"E:\SIH FINAL\codes\hottime.py"
            threading.Thread(target=run_streamlit_script, args=(script_path,)).start()

        st.write("Click the button to launch the dashboard in a new process.")
    else:
            # Message if user tries to access services without logging in
            st.warning("You must log in or sign up to access the Dashboard.")


# Streamlit page setup
elif selected_page == "Booking Slot":
    create_db()
    
    st.title('Post Office Slot Booking')

    # Dropdown for types of person
    person_types = ['Individual', 'Business', 'Government', 'Handicap Persons', 'Senior Citizens', 'Pregnant Women']
    person_type = st.selectbox('Select type of person', person_types)

    # Input fields for name, contact number, and age
    name = st.text_input('Name')
    contact_number = st.text_input('Contact Number')
    age = st.number_input('Age', min_value=0, max_value=120, step=1)

    # Get available slots by removing already booked slots
    available_slots = get_available_slots()

    # Display available time slots
    if available_slots:
        slot_time = st.selectbox('Select slot time', available_slots)

        # Display "Book Slot" button only if a slot is selected
        if st.button('Book Slot'):
            if slot_time:
                # Check if the name or contact number already exists in the bookings
                if is_name_or_contact_existing(name, contact_number):
                    st.error(f"Booking is not allowed. This slot is already Booked")
                else:
                    conn = sqlite3.connect(r"E:\SIH FINAL\codes\real.db")
                    cursor = conn.cursor()
                    cursor.execute('SELECT slot_time FROM bookings WHERE slot_time = ?', (slot_time,))
                    existing_booking = cursor.fetchone()
                    conn.close()

                    if existing_booking:
                        st.error(f"The selected slot {slot_time} is already booked. Please choose another slot.")
                    else:
                        # Proceed with booking
                        if name and contact_number and age and person_type:
                            insert_booking(name, contact_number, age, slot_time, person_type)
                            write_to_csv(name, contact_number, age, slot_time, person_type)  # Save to CSV
                            st.success(f"Booking successful! Your slot: {slot_time} for {person_type} has been booked.")
                        else:
                            st.error('Please fill all the fields.')

    # Display all the bookings (optional)
    st.subheader('Booking List')
    conn = sqlite3.connect(r"E:\SIH FINAL\codes\real.db")
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM bookings')
    bookings = cursor.fetchall()

    # Display the bookings in a table format
    if bookings:
        st.table(bookings)
    else:
        st.write("No bookings yet.")

    conn.close()
# Page for Login/Sign Up
elif selected_page == "Login/Sign Up" and not st.session_state.get("authenticated", False):
    st.header("Authentication Required")
    auth_choice = st.radio("Choose an option:", ["Login", "Sign Up"])

    if auth_choice == "Login":
        # Assuming login function is defined elsewhere
        login()

    elif auth_choice == "Sign Up":
        # Assuming signup function is defined elsewhere
        signup()

import runpy
import threading

def run_scripts_concurrently():
    # Define the paths to the scripts as a list of individual script paths
    script_paths = [
        r"E:\SIH FINAL\codes\cam.py",
        r"E:\SIH FINAL\codes\mail2.py",
        #r"E:\SIH FINAL\codes\whatsapp.py",
        #r"E:\SIH FINAL\codes\sound.py",
    ]
    
    def run_script(script_path):
        try:
            print(f"Starting script: {script_path}")
            runpy.run_path(script_path)
            print(f"Finished script: {script_path}")
        except Exception as e:
            print(f"Error running script {script_path}: {e}")

    # Create and start threads for each script
    threads = []
    for script_path in script_paths:
        thread = threading.Thread(target=run_script, args=(script_path,))
        threads.append(thread)
        thread.start()  # Start each thread

    # Wait for all threads to finish
    for thread in threads:
        thread.join()

    print("All scripts have been executed concurrently.")

# Run the function to execute scripts concurrently
run_scripts_concurrently()



# Footer HTML
footer = """
<style>
    .footer {
        position: fixed;
        bottom: 0;
        left: 0;
        right: 0;
        background-color: #f1f1f1;
        text-align: center;
        padding: 10px 0;
        font-size: 16px;
        color: #333;
        border-top: 1px solid #ddd;
        box-shadow: 0 -2px 5px rgba(0, 0, 0, 0.1);
    }
    a.footer-link {
        text-decoration: none;
        color: #007BFF;
    }
    a.footer-link:hover {
        text-decoration: underline;
    }
</style>
<div class="footer">
    <p>
        © 2024 India Post Demo. All Rights Reserved. |
        <a class="footer-link" href="mailto:support@indiapostdemo.com">Contact Us</a> |
        <a class="footer-link" href="https://www.indiapost.gov.in/" target="_blank">Visit Official Site</a>
    </p>
</div>
"""

# Inject footer into Streamlit app
st.markdown(footer, unsafe_allow_html=True)



