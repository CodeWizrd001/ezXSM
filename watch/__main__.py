import time
import os
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler

from pathlib import Path

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def compileSPLFile(filePath,change,typ) :
    print(f"{bcolors.OKBLUE}[{time.ctime()}] [!] {typ.upper()} File {filePath} {change}")
    print(f"{bcolors.FAIL}")
    os.system(f"./myexpos/{typ}/{typ} {filePath}")
    print(f"{bcolors.OKGREEN}[{time.ctime()}] [+] {typ.upper()} File {filePath} Compiled")

def on_created(event):
    fileModified = event.src_path
    if '.spl $' in fileModified + " $" :
        compileSPLFile(fileModified,"Created","spl")
    elif '.expl $' in fileModified + " $" :
        compileSPLFile(fileModified,"Created","expl")

def on_modified(event):
    fileModified = event.src_path
    if '.spl $' in fileModified + " $" :
        compileSPLFile(fileModified,"Modified","spl")
    elif '.expl $' in fileModified + " $" :
        compileSPLFile(fileModified,"Modified","expl")

def on_moved(event):
    fileModified = event.dest_path
    if '.spl $' in fileModified + " $" :
        compileSPLFile(fileModified,"Moved","spl")
    elif '.expl $' in fileModified + " $" :
        compileSPLFile(fileModified,"Moved","expl")

def on_deleted(event):
    pass
    # print(f"Deleted {event.src_path}!")

if __name__ == "__main__":
    patterns = "*"
    ignore_patterns = ""
    ignore_directories = False
    case_sensitive = True
    my_event_handler = PatternMatchingEventHandler(patterns, ignore_patterns, ignore_directories, case_sensitive)
    my_event_handler.on_created = on_created
    my_event_handler.on_deleted = on_deleted
    my_event_handler.on_modified = on_modified
    my_event_handler.on_moved = on_moved
    path = "."
    go_recursively = True
    my_observer = Observer()
    my_observer.schedule(my_event_handler, path, recursive=go_recursively)
    my_observer.start()

    if not Path("splconstants.cfg").is_file() : 
        os.system("cp myexpos/spl/splconstants.cfg ./")
    if not Path("expl-bin").is_file() :
        os.system("cp myexpos/expl/expl-bin ./")
        os.system("cp myexpos/expl/ltranslate ./")
    if not Path("expl-bin").is_file() or not Path("splconstants.cfg").is_file() :
        print(f"{bcolors.FAIL}[!!] Important Files Missing")
        print("[!] Make sure file 'splconstants.cfg','expl-bin' and 'ltranslate' exist")
    
    print(f"{bcolors.OKGREEN} [+] Watch Started")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        my_observer.stop()
        my_observer.join()