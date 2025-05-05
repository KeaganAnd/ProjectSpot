import datetime
import os

if not os.path.exists("logs"):
    os.makedirs("logs")

# Get current date and time
now = str(datetime.datetime.now()).replace(" ","_").replace(":",".")
with open(f"logs/{now}.log", "w") as file:
    file.close()

def writeLog(messageContent):
    with open(f"logs/{now}.log", "a") as file:
        file.write(f"[{datetime.datetime.now().strftime("%H:%M:%S")}]     {messageContent}\n")
        file.close()