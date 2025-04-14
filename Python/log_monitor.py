'''
Here's a practical Python script for DevOps practice: a log monitoring script that watches a log file 
(e.g., /var/log/syslog, /var/log/nginx/access.log, or any application log) in real-time and sends an alert (prints or logs) 
if it detects a keyword like "ERROR" or "CRITICAL".
'''

import time
import os 
import threading

def monitor_log(file_path, keywords=None, sleep_interval=1):
    if keywords is None:
        keywords = ["ERROR", "CRITICAL", "FAILED"]
    print(f"Monitoring Log file {file_path}")
    try:
        with open(file_path, 'r') as file:
            file.seek(0, os.SEEK_END)
            while True:
                line = file.readline()
                if not line:
                    time.sleep(sleep_interval)
                    continue
                for keyword in keywords:
                    if keyword in line:
                        print(f"[ALERT] Detected '{keyword}' in log: {line.strip()}")
    except FileNotFoundError:
        print(f"Log not found {file_path}")
    except KeyboardInterrupt:
        print(f"\n Log Monitoring Stopped")

# Monitoring Multiple Log Files using Threading Module

def start_monitoring(log_files, keywords=None):
    threads = []
    for file_path in log_files:
        t = threading.Thread(target=monitor_log, args=(file_path, keywords))
        t.daemon = True
        t.start()
        threads.append(t)
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n Monitoring interrupted by user. Exiting ...")

if __name__ == "__main__":
    log_files = [
        "/var/log/syslog",
        "/var/log/auth.log"
    ]
    keywords = ["ERROR", "CRITICAL", "FAILED"]
    start_monitoring(log_files, keywords)
