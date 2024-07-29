import time
import os
from datetime import datetime
from watchdog.observers import Observer  #watchdoglibrary
from watchdog.events import FileSystemEventHandler

class FileModifiedHandler(FileSystemEventHandler): #base class for handling system  events like modify/create/delete/moving
    def __init__(self, file_path):
        self.file_path = file_path
        self.last_modified_time = os.path.getmtime(file_path)
        self.last_size = os.path.getsize(file_path)
  

    def on_modified(self, event):
        if event.src_path == self.file_path:
            current_modified_time = os.path.getmtime(self.file_path)
            current_size = os.path.getsize(self.file_path)
            if current_modified_time != self.last_modified_time or current_size != self.last_size: #checking the diff between cur and last timestamp
                timestamp = datetime.fromtimestamp(current_modified_time).strftime('%d-%m-%y %H:%M:%S')
                print(f"File '{self.file_path}' modified at {timestamp}")
                self.last_modified_time = current_modified_time
                self.last_size = current_size

def monitor_file(file_path):
    if not os.path.exists(file_path):
        print(f"File '{file_path}' does not exist.") #checking file existance
        return

    event_handler = FileModifiedHandler(file_path) #event-handler instance of what event we are using
    observer = Observer() #objet of watchdog which do the work of monitoring
    observer.schedule(event_handler, path=os.path.dirname(file_path), recursive=False) #schedule to watch the monitoring of file take two arguments
    observer.start()
    print(f"Started monitoring file:")
    try:
        while True:
            time.sleep(1) #pause for 1 sec to reduce the overusage of cpu consumtion 
    except KeyboardInterrupt:
        observer.stop()  #stop the modify ctrl+c
    observer.join()

if __name__ == "__main__":

    file_path = "/workspaces/grafana-exporters/naveen.txt" #file path-ensure full path given
    monitor_file(file_path)

