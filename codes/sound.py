import os
import time
import pyttsx3  # For text-to-speech
import winsound  # For sound alerts (Windows-specific)
from datetime import datetime, timedelta


# Path to the snapshot folder
snapshot_path = r"E:\SIH FINAL\data\alerts"  # Folder containing snapshots

# Message to announce
alert_message = "People are overloaded. Please manage the counter queue, or add an extra counter , please solve this issue."

# Function to get the latest snapshot file in the folder
def get_latest_snapshot(folder_path, last_detected_snapshot=None):
    try:
        # Get all files in the folder
        files = [os.path.join(folder_path, f) for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]
        if not files:
            return None

        # Sort files by modification time (newest first)
        latest_file = max(files, key=os.path.getmtime)

        # Check if the latest file is different from the last detected snapshot
        if latest_file != last_detected_snapshot:
            return latest_file

        return None  # No new snapshot
    except Exception as e:
        print(f"Error fetching the latest snapshot: {e}")
        return None

# Function to trigger sound and speak the alert message
def trigger_alert(message):
    try:
        # Play a beep sound
        duration = 1000  # milliseconds
        frequency = 750  # Hz
        winsound.Beep(frequency, duration)

        # Use text-to-speech to speak the alert
        engine = pyttsx3.init()
        engine.say(message)
        engine.runAndWait()
    except Exception as e:
        print(f"Error during alert: {e}")

# Function to monitor the folder for new snapshots
def monitor_folder_for_snapshots(snapshot_path, check_interval_seconds=10, alert_interval_minutes=10):
    last_detected_snapshot = None  # Track the last detected snapshot file path
    last_alert_time = None  # Track the time of the last alert

    try:
        print("Monitoring folder for new snapshots...")

        while True:
            # Get the latest snapshot
            snapshot_file_path = get_latest_snapshot(snapshot_path, last_detected_snapshot)

            if snapshot_file_path:
                print(f"New snapshot detected: {snapshot_file_path}")

                # Check if enough time has passed since the last alert
                if last_alert_time is None or datetime.now() - last_alert_time >= timedelta(minutes=alert_interval_minutes):
                    # Trigger the alert
                    trigger_alert(alert_message)

                    # Update the last alert time
                    last_alert_time = datetime.now()

                # Update the last detected snapshot
                last_detected_snapshot = snapshot_file_path

            else:
                print("")

            # Wait before checking again
            time.sleep(check_interval_seconds)

    except KeyboardInterrupt:
        print("Monitoring stopped by user.")
    except Exception as e:
        print(f"Error during monitoring: {e}")

# Example usage: Call the function to start monitoring the folder
monitor_folder_for_snapshots(snapshot_path, check_interval_seconds=10, alert_interval_minutes=10)
