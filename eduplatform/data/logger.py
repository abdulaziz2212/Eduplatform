import os
from datetime import datetime

def log_export(action, format, filename):
    os.makedirs("logs", exist_ok=True)
    with open("logs/export_log.txt", "a", encoding="utf-8") as log:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log.write(f"[{timestamp}] {action.upper()} - {format.upper()} - {filename}\n")
