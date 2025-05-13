import datetime
import os

if not os.path.exists("logs"):
    os.makedirs("logs")     #Looks to see if a logs folder exists and creates if it doesnt


maxLogs = 10   #How many logs the system will keep, deleting the oldest ones

logsInDir = os.listdir("logs") #Fetches all logs from the log folder

if len(logsInDir) >= maxLogs:
    for log in logsInDir[:-(maxLogs-1)]: #Logs fetched with newest ones first in list.
        if log != "latest.log":
            os.remove(f"logs/{log}")         # Gets rid of any log that isnt the 10 most recent


for log in logsInDir:
    if log == "latest.log":                     #Looks for the last sessions log being latest.log
        with open(f"logs/latest.log", "r") as log:
            firstLine = log.readline()          #Reads the first line which has the date the file was created
        try:
            os.rename(f"logs/latest.log", f"logs/{firstLine[:firstLine.index("|")-1]}.log") #Renames the latest log to its date and time created
        except Exception:
            os.rename(f"logs/latest.log", f"logs/olderLog.log") #If the first line doesnt exist then just name it generically


# Get current date and time
now = str(datetime.datetime.now()).replace(" ","_").replace(":",".") #Removes spaces and : because windows file system doesnt like them
with open(f"logs/latest.log", "w") as file:                          #Makes latest log 
    file.write(f"{now} | Max Of {maxLogs} Logs\n")                   #Writes date to top line
    file.close()

def writeLog(messageContent, preventRecursive = False):
    with open(f"logs/latest.log", "a") as file:
        try: 
            file.write(f"[{datetime.datetime.now().strftime("%H:%M:%S")}]     {messageContent}\n") #If no error write log to file
            file.close()
        except Exception as e: #If an error occurs while writing it writes the error to the file
            if preventRecursive: #Prevents infinite error loop
                writeLog(f"{datetime.datetime.now().strftime("%H:%M:%S")}     Encountered Error When Saving To Log | {e}\n", True)