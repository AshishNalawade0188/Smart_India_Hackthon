
import runpy
import threading

def run_script(script_path):
    try:
        print(f"Starting script: {script_path}")
        runpy.run_path(script_path)
        print(f"Finished script: {script_path}")
    except Exception as e:
        print(f"Error running script {script_path}: {e}")

# Define the paths to the scripts as a list of individual script paths
script_paths = [
    r"E:\SIH FINAL\codes\main.py"
    
]

# Create threads for each script
threads = []
for script_path in script_paths:
    thread = threading.Thread(target=run_script, args=(script_path,))
    threads.append(thread)
    thread.start()  # Start each thread 


# Wait for all threads to finish
for thread in threads:
    thread.join()

print("All scripts have been executed concurrently.")