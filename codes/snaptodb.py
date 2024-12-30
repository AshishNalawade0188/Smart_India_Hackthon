import sqlite3
import os

# Path to your existing database
DB_PATH = r'E:\SIH FINAL\codes\real.db'

# Path to the alerts folder where .jpg files are saved
ALERTS_FOLDER = r'C:\Users\sakshi\OneDrive\Desktop\post office\data\alerts'

# Function to get the latest .jpg file in the alerts folder
def get_latest_jpg_file():
    # List all files in the 'alerts' folder that end with .jpg
    jpg_files = [f for f in os.listdir(ALERTS_FOLDER) if f.lower().endswith('.jpg')]
    
    if not jpg_files:
        return None  # No .jpg files found

    # Sort files by modification date (most recent first)
    jpg_files.sort(key=lambda f: os.path.getmtime(os.path.join(ALERTS_FOLDER, f)), reverse=True)

    # Get the most recent file path
    latest_file = jpg_files[0]
    return os.path.join(ALERTS_FOLDER, latest_file)

# Function to create the snapshot_table in the database
def create_snapshot_table():
    # Connect to the SQLite database
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Create snapshot_table if it doesn't exist
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS snapshot_table (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        image_path TEXT NOT NULL
    )
    ''')

    # Commit changes and close the connection
    conn.commit()
    conn.close()

# Function to store the image path in the snapshot_table of the database
def store_image_path_in_db(image_path):
    # Connect to the SQLite database
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Insert the image path into the snapshot_table
    cursor.execute('''
    INSERT INTO snapshot_table (image_path)
    VALUES (?)
    ''', (image_path,))

    # Commit changes and close the connection
    conn.commit()
    conn.close()

# Function to check the latest image and store its path in the database
def update_snapshot_table():
    # Create the snapshot_table if it doesn't exist
    create_snapshot_table()
    
    # Get the latest .jpg file in the alerts folder
    latest_image_path = get_latest_jpg_file()
    
    if latest_image_path:
        # Store the latest image path in the database
        store_image_path_in_db(latest_image_path)
        print(f"Image path {latest_image_path} stored successfully in the database.")
    else:
        print("No .jpg files found in the alerts folder.")

# Main function to run the program
if __name__ == "__main__":
    update_snapshot_table()
