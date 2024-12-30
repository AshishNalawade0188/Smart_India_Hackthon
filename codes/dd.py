import sqlite3
import os

# Define the path to your database
db_path = os.path.abspath(r"E:\SIH FINAL\codes\real.db")

# Connect to the database
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Table name to be dropped
table_name = "queue_data"  # Replace with the actual table name, e.g., "queue_data" or "alerts"

try:
    # Drop the table if it exists
    cursor.execute(f"DROP TABLE IF EXISTS {table_name}")
    print(f"Table '{table_name}' has been dropped successfully.")
except sqlite3.Error as e:
    print(f"An error occurred while dropping the table: {e}")

# Commit and close the connection
conn.commit()
conn.close()
