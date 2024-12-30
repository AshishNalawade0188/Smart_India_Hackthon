import os
import cv2
import time
import sqlite3
from datetime import datetime
from ultralytics import YOLO

# Paths
model_path = os.path.abspath(r"E:\My Projects\SIH FINAL\SIH FINAL\Trained model\yolo_person.pt")
alert_folder_path = os.path.abspath(r"E:\My Projects\SIH FINAL\SIH FINAL\data\alerts")
db_path = os.path.abspath(r"E:\My Projects\SIH FINAL\SIH FINAL\codes\real.db")

# Create necessary folders if they don't exist
os.makedirs(alert_folder_path, exist_ok=True)

# Initialize SQLite database
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Create tables if they don't exist
cursor.execute('''CREATE TABLE IF NOT EXISTS QUEUE_TABLE (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date TEXT,
    time TEXT,
    number_of_people INTEGER,
    difference_in_count INTEGER
)''')

cursor.execute('''CREATE TABLE IF NOT EXISTS alerts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp TEXT,
    snapshot_path TEXT
)''')

conn.commit()

# Load the YOLOv8 model
print("Loading YOLO model...")
try:
    model = YOLO(model_path)
    print("Model loaded successfully!")
except Exception as e:
    print(f"Error loading YOLO model: {e}")
    exit()

# Access the live camera (use index 0 for the default camera)
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Error accessing the camera. Please check your device.")
    exit()

# Get camera properties
fps = cap.get(cv2.CAP_PROP_FPS) or 30  # Default to 30 FPS if unavailable
frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

# Initialize variables
frame_count = 0  # Frame counter for naming alert snapshots
last_snapshot_time = 0  # Timestamp of the last snapshot
snapshot_delay = 30  # Delay between snapshots in seconds
last_db_save_time = time.time()  # Timestamp for database saving
db_save_interval = 300  # Save data every 5 minutes (300 seconds)
last_people_count = 0  # To calculate the difference in count

# Define the queue area as a rectangle (percentage of the frame size)
queue_top = int(frame_height * 0.1)  # 10% from the top
queue_bottom = int(frame_height * 0.9)  # Increased to 90% from the top
queue_left = int(frame_width * 0.15)  # Increased to 15% from the left
queue_right = int(frame_width * 0.85)  # Increased to 85% from the left

# Define the queue area rectangle for visualization
queue_area = (queue_left, queue_top, queue_right, queue_bottom)

print("Starting live video processing...")
try:
    while True:
        # Capture frame-by-frame
        ret, frame = cap.read()
        if not ret:
            print("Failed to read frame from the camera.")
            break

        # Detect objects using YOLO
        results = model.predict(source=frame, conf=0.5, show=False)  # Adjust `conf` as needed
        detections = results[0].boxes.xyxy.cpu().numpy()  # Get bounding boxes
        num_people_in_queue = 0  # Counter for people in the queue area

        # Draw the queue area rectangle on the frame
        cv2.rectangle(frame, (queue_left, queue_top), (queue_right, queue_bottom), (255, 0, 0), 2)
        cv2.putText(frame, "Queue Area", (queue_left + 5, queue_top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 0, 0), 2)

        # Display the maximum threshold value at the top-right corner
        cv2.putText(frame, "Max : 3", (frame_width - 200, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)

        # Process each detected object
        for det in detections:
            x1, y1, x2, y2 = map(int, det[:4])  # Extract coordinates
            # Check if the person is inside the queue area
            if x2 > queue_left and x1 < queue_right and y2 > queue_top and y1 < queue_bottom:
                num_people_in_queue += 1
                # Draw bounding boxes around detected people
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.putText(frame, "Person", (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

        # Display the number of people in the queue area at the bottom-left corner
        cv2.putText(frame, f"Queue People Count: {num_people_in_queue}", (10, frame_height - 20), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

        # Alert: Save snapshot if people count exceeds the threshold and delay is respected
        current_time = time.time()
        if num_people_in_queue > 3 and (current_time - last_snapshot_time > snapshot_delay):
            alert_snapshot_path = os.path.join(alert_folder_path, f"alert_frame_{time.strftime('%Y%m%d_%H%M%S')}.jpg")
            cv2.imwrite(alert_snapshot_path, frame)
            last_snapshot_time = current_time  # Update the last snapshot time
            cursor.execute('''INSERT INTO alerts (timestamp, snapshot_path) VALUES (?, ?)''',
                           (datetime.now().strftime("%Y-%m-%d %H:%M:%S"), alert_snapshot_path))
            conn.commit()
            print(f"Alert: People count exceeded threshold. Snapshot saved to {alert_snapshot_path}")

        # Save data to the database every 5 minutes
        if current_time - last_db_save_time >= db_save_interval:
            date_str = datetime.now().strftime("%Y-%m-%d")
            time_str = datetime.now().strftime("%H:%M:%S")
            count_diff = num_people_in_queue - last_people_count
            cursor.execute('''INSERT INTO queue_data (date, time, number_of_people, difference_in_count) VALUES (?, ?, ?, ?)''',
                           (date_str, time_str, num_people_in_queue, count_diff))
            conn.commit()
            print(f"Data saved to database: Date={date_str}, Time={time_str}, People={num_people_in_queue}, Diff={count_diff}")
            last_db_save_time = current_time
            last_people_count = num_people_in_queue

        # Display the live video feed with detections
        cv2.imshow("Live Video Feed", frame)

        # Break the loop if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        frame_count += 1

except Exception as e:
    print(f"An error occurred: {e}")
finally:
    # Release the capture and close any OpenCV windows
    cap.release()
    cv2.destroyAllWindows()
    conn.close()
    print(f"Alert snapshots saved in: {alert_folder_path}")
    print(f"Database updated at: {db_path}")
