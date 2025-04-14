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

### Python Tuples ###
A tuple is an immutable (unchangeable) ordered collection of elements in Python. It is similar to a list, but unlike lists, tuples cannot be modified after creation.

*Creating a Tuple*
```python
# Different ways to create a tuple
t1 = (1, 2, 3)       # With parentheses
t2 = 1, 2, 3         # Without parentheses
t3 = tuple([1, 2, 3]) # Using the tuple() constructor
t4 = ("hello",)      # Single-element tuple (comma is needed)

print(t1)  # (1, 2, 3)
print(t2)  # (1, 2, 3)
print(t3)  # (1, 2, 3)
print(t4)  # ('hello',)
```

*Accessing Elements in a Tuple*
```python
t = (10, 20, 30, 40)

print(t[0])  # 10
print(t[2])  # 30
```

*Tuple Slicing*
```python
t = (10, 20, 30, 40, 50, 60)

print(t[1:4])   # (20, 30, 40) -> From index 1 to 3
print(t[:3])    # (10, 20, 30) -> First three elements
print(t[3:])    # (40, 50, 60) -> From index 3 to end
print(t[::-1])  # (60, 50, 40, 30, 20, 10) -> Reversed tuple
```

*Tuple Unpacking*
```python
t = (100, 200, 300)

a, b, c = t  # Unpacking
print(a)  # 100
print(b)  # 200
print(c)  # 300
```
```python
t = (1, 2, 3)
a, _, c = t  # Ignore the second value
print(a, c)  # 1 3
```

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

*Accessing Values*
- `get()` is safer than `[]` because it returns None if the key is missing instead of throwing an error.
```python
print(student["name"])   # Output: Alice
print(student.get("age"))  # Output: 25
```
```python
print(student.get("marks", 100) # As Marks key not in Dictionary so it will return 100
```

*Looping Through a Dictionary*
```python
for key, value in student.items():
    print(f"{key}: {value}")
```

---

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

---

The **subprocess** module in Python is used to execute shell commands, interact with system processes, and capture their output.
```python
import subprocess

subprocess.run(["echo", "Hello, DevOps!"])
```
```bash
Hello, DevOps!
```

*Capturing Command Output (capture_output=True)*
```python
result = subprocess.run(["ls", "-l"], capture_output=True, text=True).stdout.strip()
print(result.stdout)  # Prints the output of the 'ls -l' command
```
- `capture_output=True` → Captures the output (instead of printing it directly).
- `text=True` → Returns output as a string instead of bytes.

*Handling Errors (check=True)*
```python
try:
    subprocess.run(["ls", "/non_existent_path"], check=True)
except subprocess.CalledProcessError:
    print("Command failed!")
```
- `check=True` raises an exception if the command fails.
---

The **shutil** module is used for high-level file operations such as copying, moving, and deleting files and directories. Below are common shutil commands with examples

*Copy Files*
```python
import shutil

shutil.copy("source.txt", "destination.txt")  # Copies file
shutil.copy2("source.txt", "destination2.txt")  # Copies file with metadata
```

*Copy Directories*
```python
shutil.copytree("source_folder", "backup_folder")
```

*Move/Rename Files and Directories*
```python
shutil.move("file.txt", "new_folder/file.txt")
```

*Delete Files and Directories*
```python
shutil.rmtree("unwanted_folder")
```

*Disk Usage Statistics*
```python
total, used, free = shutil.disk_usage("/")
print(f"Total: {total}, Used: {used}, Free: {free}")
```

---

### Threading in Python ###
Threading is a way to run multiple operations at the same time within a single Python process — like multitasking inside your code.

**Why Use Threading?**

Imagine you're:
- Watching multiple log files (log1, log2, log3)
- Each file is getting updated constantly

Without threading:
- You'd have to monitor one file at a time (slow, inefficient)

With threading:
- You can monitor all files at once, each in its own thread
- Faster, real-time performance for tasks like log monitoring, web scraping, background jobs, etc.

- *Python has a Global Interpreter Lock (GIL), so CPU-bound tasks aren't fully parallel with threads — but I/O-bound tasks (like log monitoring, file read/write, network calls) work great with threading.*
- *For CPU-heavy tasks, use `multiprocessing` instead of `threading`.*

```python
import threading
import time

def say_hello():
    for i in range(5):
        print("Hello")
        time.sleep(1)

def say_bye():
    for i in range(5):
        print("Bye")

# Run Both functions in Parallel using Threads
t1 = threading.Thread(target=say_hello)
t2 = threading.Thread(target=say_bye)

t1.start()
t2.start()

t1.join()
t2.join()

print("Done")
```

---

