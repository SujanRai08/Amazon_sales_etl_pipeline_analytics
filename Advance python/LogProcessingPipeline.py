"""Description:
This project demonstrates advanced Python concepts in
 building a pipeline to process large server logs efficiently.
 It extracts error information, transforms it into structured JSON, and loads the processed data into a SQLite database."""

"""
This project uses:

Generators for memory-efficient log reading.
Context Managers for resource handling.
Decorators for logging execution.
Regular Expressions for log parsing.
SQLite Integration for data storage.
Multithreading for concurrent processing.

"""
import re
import json
import sqlite3
import threading
from datetime import datetime

# Context Manager for Database Connection
class DatabaseManager:
    def __init__(self, db_path):
        self.db_path = db_path

    def __enter__(self):
        self.conn = sqlite3.connect(self.db_path)
        self.cursor = self.conn.cursor()
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS logs (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                timestamp TEXT,
                                level TEXT,
                                message TEXT)''')
        return self.cursor

    def __exit__(self, exc_type, exc_value, traceback):
        self.conn.commit()
        self.conn.close()


# Decorator for Logging Execution
def log_execution(func):
    def wrapper(*args, **kwargs):
        print(f"[{datetime.now()}] Starting {func.__name__}...")
        result = func(*args, **kwargs)
        print(f"[{datetime.now()}] Finished {func.__name__}.")
        return result
    return wrapper


# Generator to Read Large Log Files
def read_logs(file_path):
    with open(file_path, "r") as file:
        for line in file:
            yield line.strip()


# Parse Log Line using Regular Expressions
def parse_log(line):
    pattern = r'(?P<timestamp>\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}) - (?P<level>\w+) - (?P<message>.+)'
    match = re.match(pattern, line)
    if match:
        return match.groupdict()
    return None


# Process Logs and Load into Database
@log_execution
def process_logs(file_path, db_path):
    with DatabaseManager(db_path) as db:
        for log in read_logs(file_path):
            parsed = parse_log(log)
            if parsed:
                db.execute('INSERT INTO logs (timestamp, level, message) VALUES (?, ?, ?)',
                           (parsed['timestamp'], parsed['level'], parsed['message']))


# Multithreaded Log Processing
@log_execution
def process_logs_concurrently(log_files, db_path):
    threads = []
    for log_file in log_files:
        thread = threading.Thread(target=process_logs, args=(log_file, db_path))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()


# Example Execution
if __name__ == "__main__":
    # Sample log files
    log_files = ["Advance python/server_log1.txt", "Advance python/server_log2.txt"]
    database_path = "processed_logs.db"

    # Process logs concurrently
    process_logs_concurrently(log_files, database_path)

    # Verify Data in Database
    with sqlite3.connect(database_path) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM logs")
        rows = cursor.fetchall()
        print(json.dumps(rows, indent=2))
