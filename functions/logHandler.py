import datetime
import os

if not os.path.exists("logs"):
    os.makedirs("logs")
import os

maxLogs = 10

logsInDir = os.listdir("logs")

if len(logsInDir) >= maxLogs:
    for log in logsInDir[:-(maxLogs-1)]:
        os.remove(f"logs/{log}")


for log in logsInDir:
    if log == "latest.log":
        with open(f"logs/{log}", "r") as log:
            firstLine = log.readline()
            print(firstLine)
        try:
            os.rename(f"logs/latest.log", f"logs/{firstLine[:firstLine.index("|")]}.log")
        except Exception:
            os.rename(f"logs/latest.log", f"logs/olderLog.log")


# Get current date and time
now = str(datetime.datetime.now()).replace(" ","_").replace(":",".")
with open(f"logs/latest.log", "w") as file:
    file.write(f"{now} | Max Of {maxLogs} Logs\n")
    file.close()

def writeLog(messageContent, preventRecursive = False):
    with open(f"logs/latest.log", "a") as file:
        try: 
            file.write(f"[{datetime.datetime.now().strftime("%H:%M:%S")}]     {messageContent}\n")
            file.close()
        except Exception as e:
            if preventRecursive:
                writeLog(f"{datetime.datetime.now().strftime("%H:%M:%S")}     Encountered Error When Saving To Log | {e}\n", True)