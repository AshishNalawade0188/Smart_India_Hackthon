

# Function to create the SQLite database and table if they don't exist
def create_db():
    conn = sqlite3.connect(r"E:\SIH FINAL\codes\post.db")
    cursor = conn.cursor()

    # Check if the 'age' column exists, and if not, add it
    cursor.execute("PRAGMA table_info(bookings)")
    columns = [column[1] for column in cursor.fetchall()]
    if 'age' not in columns:
        cursor.execute('''
        ALTER TABLE bookings ADD COLUMN age INTEGER NOT NULL DEFAULT 0
        ''')

    # Create the table if it doesn't exist
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS bookings (
        booking_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        contact_number TEXT NOT NULL,
        age INTEGER NOT NULL,
        slot_time TEXT NOT NULL,
        person_type TEXT NOT NULL
    )
    ''')
    
    conn.commit()
    conn.close()

# Function to insert a new booking into the database
def insert_booking(name, contact_number, age, slot_time, person_type):
    conn = sqlite3.connect(r"E:\SIH FINAL\codes\post.db")
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO bookings (name, contact_number, age, slot_time, person_type)
        VALUES (?, ?, ?, ?, ?)
    ''', (name, contact_number, age, slot_time, person_type))
    conn.commit()
    conn.close()

# Function to get available slots, removing already booked times
def get_available_slots():
    booked_slots = []
    conn = sqlite3.connect(r"E:\SIH FINAL\codes\post.db")
    cursor = conn.cursor()
    cursor.execute('SELECT slot_time FROM bookings')
    booked_slots = [slot[0] for slot in cursor.fetchall()]
    conn.close()

    # Generate time slots every 10 minutes for the next 12 hours
    current_time = datetime.now()
    available_slots = []
    
    for i in range(12 * 6):  # 12 hours, 6 intervals per hour
        slot_time = (current_time + timedelta(minutes=10 * i)).strftime("%I:%M %p")
        if slot_time not in booked_slots:
            available_slots.append(slot_time)

    return available_slots

# Initialize database (create if not exists)
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
slot_time = st.selectbox('Select slot time', available_slots)

# Submit button for booking slot
if st.button('Book Slot'):
    if name and contact_number and age and slot_time and person_type:
        # Check if the selected time slot is already booked
        conn = sqlite3.connect(r"E:\SIH FINAL\codes\post.db")
        cursor = conn.cursor()
        cursor.execute('SELECT slot_time FROM bookings WHERE slot_time = ?', (slot_time,))
        existing_booking = cursor.fetchone()
        conn.close()

        if existing_booking:
            st.error(f"The selected slot {slot_time} is already booked. Please choose another slot.")
        else:
            # Proceed with booking as there's no 10-minute restriction
            insert_booking(name, contact_number, age, slot_time, person_type)
            st.success(f"Booking successful! Your slot: {slot_time} for {person_type} has been booked.")
    else:
        st.error('Please fill all the fields.')

# Display all the bookings (optional)
st.subheader('Booking List')
conn = sqlite3.connect(r"E:\SIH FINAL\codes\post.db")
cursor = conn.cursor()
cursor.execute('SELECT * FROM bookings')
bookings = cursor.fetchall()

# Display the bookings in a table format
if bookings:
    st.table(bookings)
else:
    st.write("No bookings yet.")

conn.close()
