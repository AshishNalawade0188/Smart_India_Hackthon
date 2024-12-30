import pywhatkit as kit
import os
import time

# Path to the snapshot folder
snapshot_path = r"E:\SIH FINAL\data\alerts"  # Folder containing snapshots

# WhatsApp configuration
receiver_numbers = ["9130320188"]  # List of receiver's phone numbers without country code
message = "Snapshot for review: People count is being overridden, Your attention is required."

# Function to get the latest snapshot file in the folder
def get_latest_snapshot(folder_path, last_sent_snapshot=None):
    try:
        # Get all files in the folder
        files = [os.path.join(folder_path, f) for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]
        if not files:
            return None

        # Sort files by modification time (newest first)
        latest_file = max(files, key=os.path.getmtime)

        # Check if the latest file is different from the last sent snapshot
        if latest_file != last_sent_snapshot:
            return latest_file

        return None  # No new snapshot
    except Exception as e:
        print(f"Error fetching the latest snapshot: {e}")
        return None

# Function to send WhatsApp alert with the latest image
def send_whatsapp_alert(snapshot_path, interval_minutes=10, max_messages=5):
    last_sent_snapshot = None  # Track the last sent snapshot file path

    try:
        # Loop to send multiple messages at specified intervals
        for i in range(max_messages):
            # Get the latest snapshot
            snapshot_file_path = get_latest_snapshot(snapshot_path, last_sent_snapshot)
            if not snapshot_file_path:
                print("No new snapshot files found in the folder or the file is the same as the last one.")
                time.sleep(interval_minutes * 60)  # Wait for the specified interval
                continue  # Skip sending the message if no new snapshot

            print(f"Sending message {i + 1}...")
            print(f"New snapshot: {snapshot_file_path}")

            # Send the snapshot with a message as caption
            for receiver_number in receiver_numbers:
                print(f"Sending snapshot to {receiver_number}...")

                try:
                    # Send the image with caption (message) using the same WhatsApp Web session
                    kit.sendwhats_image(
                        f"+{receiver_number}",  # Phone number with country code
                        snapshot_file_path,  # Path to the image
                        caption=message,  # Message as caption
                        wait_time=10,  # Wait time for WhatsApp Web to load
                        close_time=3   # Time to keep the browser tab open before closing
                    )
                    time.sleep(3)  # Slight delay to prevent message flooding
                except Exception as send_error:
                    print(f"Error sending snapshot to {receiver_number}: {send_error}")

            # Update the last sent snapshot to the current one
            last_sent_snapshot = snapshot_file_path

            # Wait for the specified interval before sending the next message
            if i < max_messages - 1:
                print(f"Waiting for {interval_minutes} minutes before checking for a new snapshot.")
                time.sleep(interval_minutes * 60)  # Convert minutes to seconds

        print("All messages and snapshots sent successfully!")

    except Exception as e:
        print(f"Error sending WhatsApp alert: {e}")

# Example usage: Call the function to send the snapshot with the message at intervals
send_whatsapp_alert(snapshot_path, interval_minutes=10, max_messages=5)