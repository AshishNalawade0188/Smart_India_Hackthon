import cv2

# Open the default camera (0 is usually the laptop camera)
camera = cv2.VideoCapture(0)

if not camera.isOpened():
    print("Error: Could not open camera.")
    exit()

while True:
    # Capture frame-by-frame
    ret, frame = camera.read()
    
    if not ret:
        print("Error: Failed to capture frame.")
        break
    
    # Get the dimensions of the frame
    height, width, _ = frame.shape
    
    # Calculate the size of each cell in the 3x3 grid
    cell_width = width // 3
    cell_height = height // 3

    # Draw horizontal lines
    for i in range(1, 3):  # Two lines to divide into three rows
        y = i * cell_height
        cv2.line(frame, (0, y), (width, y), (0, 255, 0), 2)

    # Draw vertical lines
    for j in range(1, 3):  # Two lines to divide into three columns
        x = j * cell_width
        cv2.line(frame, (x, 0), (x, height), (0, 255, 0), 2)
    
    # Display the frame with grid
    cv2.imshow('Laptop Camera with 3x3 Grid', frame)
    
    # Press 'q' to quit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the camera and close all OpenCV windows
camera.release()
cv2.destroyAllWindows()
