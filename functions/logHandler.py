import datetime
import os

# Create the "logs" directory if it doesn't exist
os.makedirs("logs", exist_ok=True)

# Generate a valid timestamp for the filename (no illegal characters)
now = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

# Define the log file path
log_file_path = f"logs/{now}.log"

# Create the log file and write a creation message
with open(log_file_path, "w") as file:
    file.write("Log file created successfully.\n")

# Define a function to write log messages
def writeLog(messageContent):
    with open(log_file_path, "a") as file:
        timestamp = datetime.datetime.now().strftime("%H:%M:%S")
        file.write(f"[{timestamp}]     {messageContent}\n")
