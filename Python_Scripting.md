### Python Strings ###
- **len() – Returns the length of a string**
  ```python
  text = "Hello, World!"
  print(len(text))  # Output: 13
  ```
- **lower() & upper()** – Converts a string to lowercase or uppercase
  ```python
  print(text.lower())  # Output: hello, world!
  print(text.upper())  # Output: HELLO, WORLD!
  ```
- **strip()** – Removes leading and trailing spaces
  ```python
  text = "   Hello   "
  print(text.strip())  # Output: "Hello"
  ```
---

### Python Dicitonary ###
A dictionary in Python is a collection of key-value pairs, where each key is unique and used to access its corresponding value.

```python
# Empty dictionary
my_dict = {}

# Dictionary with values
student = {
    "name": "Alice",
    "age": 25,
    "course": "Computer Science"
}
print(student)  
# Output: {'name': 'Alice', 'age': 25, 'course': 'Computer Science'}
```

- Accessing Values. `get()` is safer than `[]` because it returns None if the key is missing instead of throwing an error.
```python
print(student["name"])   # Output: Alice
print(student.get("age"))  # Output: 25
```

**Slicing [START:STOP:STEP]**
- start: Where to start slicing (default is 0).
- stop: Where to stop slicing (default is len(sequence)).
- step: The increment (negative values reverse the sequence).

*String Reversal*
```python
text = "Python"
reversed_text = text[::-1]
print(reversed_text)  # Output: nohtyP
```

**input()** function is used to take user input from the keyboard. By default, it returns the input as a string.
```python
name = input("Enter your name: ")
print("Hello, " + name + "!")
```
```python
age = int(input("Enter your age: "))  # Converts input to an integer
height = float(input("Enter your height in meters: "))  # Converts input to a float
```

**seek()** method is used with file objects to change the current file position. This is useful when you need to move to a specific location in a file for reading or writing.
```python
file.seek(offset, whence)
```
- offset – Number of bytes to move.
- whence (optional) – Reference position:
  - 0 (default) – Start of the file.
  - 1 – Current position.
  - 2 – End of the file.
- `os.SEEK_END` is a constant used with the seek() method to move the file pointer relative to the end of the file.
```python
with open("example.txt", "a+") as f:
    f.seek(0, os.SEEK_END)  # Move to the end of file
    f.write("\nNew line at the end")
```

**readline()** is a built-in method in Python used to read one line at a time from a file. The file pointer moves to the next line after reading.
```python
file.readline()
```

**time**
- *time.sleep()* function is used to pause the execution of a program for a specified amount of time
```python
time.sleep(3) # Pause for 3 seconds
```

You need to write a Python script to monitor a log file in real time and trigger an alert if a specific keyword (e.g., `"ERROR"`) appears.
- Continuously monitor a log file (e.g., `/var/log/syslog`) for new entries.
- If the word "ERROR" appears, print an alert message and write the event to another file (`error_log.txt`).
- Implement exception handling to avoid crashes if the log file is rotated or deleted.
```python
import os
import time

LOG_FILE = "/var/log/syslog"
ERROR_LOG_FILE = "error_log.txt"
KEYWORD = "ERROR"

def monitor_log(file_path):
    try:
        with open(file_path, "r") as log_file:
            log_file.seek(0, os.SEEK_END)
            
            while True:
                line = log_file.readline()
                if not line:
                    time.sleep(1)
                    continue
                if KEYWORD in line:
                    print(f"Alert Keyword: {KEYWORD} detected: {line.strip()}")
                    with open(ERROR_LOG_FILE, "a") as error_file:
                        error_file.write(line)
    except FileNotFoundError:
        print(f"[ERROR] Log File {file_path} not found, Retrying in 5 Seconds ...")
        time.sleep(5)
        monitor_log(file_path)
    except PermissionError:
        print(f"[ERROR] Permission Denied while accessing File {file_path}")
    except Exception as e:
        print(f"[ERROR] Unexpected Error: {e}")

if __name__ == "__main__":
    monitor_log(LOG_FILE)
```
