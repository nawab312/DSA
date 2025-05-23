**`xargs`** is a command in Linux that allows you to take standard input (stdin) and convert it into command-line arguments for another command. It's useful for handling large lists of arguments that might exceed the shell's command-line length limit.
- ```bash
  echo "file1 file2 file3" | xargs rm
  ```
  This deletes file1, file2, and file3 by passing them as arguments to rm.
- ```bash
  ls | xargs -n 2 echo
  ```
  ```bash
  #Output
  script1.sh script2.sh
  script3.sh script4.sh
  script5.sh
  ```
  Processes two filenames at a time.
- ```bash
  ls | xargs -I {} echo {}
  ```
  ```bash
  #Output
  script1.sh
  script2.sh
  script3.sh
  script4.sh
  script5.sh
  ```
  Each `{}` is replaced with an individual file.
- ```bash
  find . -name "*.log" | xargs rm
  ```

---

## Linux File System & Management ##

### File & Directory Commands ###

The **`ls`** (list) command is used to list files and directories in Linux.

![image](https://github.com/user-attachments/assets/1e26b883-0281-47f1-af04-31df3fba16a3)


The **`head`** and **`tail`** commands are used for viewing specific parts of a file or command output in Linux.
```bash
head -n <number_of_lines> <file>
```
- View the first 10 lines of a file (default)
  ```bash
  head /etc/passwd
  ```
- View the first 5 lines of a file:
  ```bash
  head -5 /var/log/syslog
  ```
- View the first 10 lines of the output of a command:
  ```bash
  ls -l | head -10
  ```
- Extract lines 5 to 10 from a file:
  ```bash
  head -10 /etc/passwd | tail -5
  ```

The **`find`** command in Linux is used to search for files and directories based on various criteria such as name, size, type, permissions, and modification time
```bash
find <directory> <options> <action>
```

![image](https://github.com/user-attachments/assets/b0082701-79a3-449c-935d-48f57169c21c)

The `-exec` option in the `find` command is used to execute a command on each file or directory found. It allows you to perform actions like deleting, moving, or modifying files that match specific criteria.
```bash
find <directory> <conditions> -exec <command> {} \;
```
- {} → Placeholder for each found file or directory.
- \; → Terminates the command execution.

Delete all .log files older than 7 days:
```bash
find /var/logs -type f -name "*.log*" -mtime +7 -exec rm {} \;
```

Using + instead of \; executes the command in batches (better performance).
```bash
find /home/user/ -type f -exec ls -lh {} +
```

---

## Linux Process Management ##

### System Resource Usage ###
**`sar`** (System Activity Reporter) command is a powerful Linux tool for monitoring system performance, including CPU, memory, disk, and network usage.
- Check CPU Usage
  - `-u` → CPU usage
  - `5` → Collect data every 5 seconds
  - `3` → Repeat 3 times
  - `%user` → CPU used by user processes
  - `%system` → CPU used by kernel
  - `%iowait` → CPU waiting for I/O
  - `%idle` → Free CPU percentage

```bash
sar -u 5 3
12:30:01 AM  CPU  %user  %nice  %system  %iowait  %steal  %idle
12:30:06 AM  all   5.23   0.00     2.11     0.45    0.00  92.21
12:30:11 AM  all   4.89   0.00     1.98     0.33    0.00  92.80
```

- Check Memory Usage
```bash
sar -r 5 3
```

**`iostat`** command in Linux is used for monitoring system input/output (I/O) device loading by observing the time devices are active in relation to their average transfer rates. It provides insights into CPU utilization and disk I/O statistics
```bash
iostat [options] [interval] [count]
```
- Basic CPU and Disk I/O Statistics. Displays CPU usage and disk I/O stats since the system was last rebooted.
  ```bash
  iostat
  ```
- Displaying Statistics in Human-Readable Format. Shows output in a human-readable format (e.g., using KB/MB instead of sectors).
  ```bash
  iostat -h
  ```
- Displaying CPU Utilization Only
  ```bash
  iostat -c
  ```
- Displaying Device Utilization Only. Displays only disk I/O statistics.
  ```bash
  iostat -d
  ```


### System Uptime ###
The **`uptime`** command in Linux provides information about how long the system has been running, along with the system load averages over the last 1, 5, and 15 minutes. It is commonly used to quickly check the system’s uptime and load.
```bash
uptime
 17:51:11 up 5 days,  1:55,  1 user,  load average: 1.13, 1.04, 0.81
```

---

## Linux Scripting ##

### Bash Scripting ###
**If-Else**

- Check if a number is positive or negative.
```bash
#!/bin/bash
echo "Enter a Number"
read num

if [ $num -gt 0 ]; then
  echo "$num is Positive Number"
elif [ $num -lt 0 ]; then
  echo "$num is Negative Number"
else
  echo "$num is Zero"
fi
```

```bash
#Output
Enter a Number
11
11 is Positive Number
```

- Check If a File Exists
  - `-f` checks if the given file exists and is a regular file.

```bash
#!/bin/bash
echo "Enter the file Name"
read file

if [ -f $file ]; then
  echo "File Exists"
else 
  echo "File doesnt Exists"
fi
```

```bash
#Output
Enter the file Name
script1.sh
File Exists

Enter the file Name
script3.sh
File doesnt Exists
```

- `(( ))` is used for arithmetic operations (ONLY FOR INTEGERS) and comparisons in `bash` (and some other shells). It's a more efficient and readable way of performing arithmetic comparisons compared to using `[ ]` or `test`.
  - You don't need to put a `$` before variables inside `(( ))` (e.g., ((a + b)) instead of (( $a + $b ))).
  - It can also be used for comparison operations like equality (`==`), inequality (`!=`), greater than (`>`), less than (`<`), and more.
  - No need for -eq, -lt, -gt, etc., when using (( )).
```bash
a=10
b=20

if (( a < b )); then
    echo "a is less than b"
fi
```

- `bc` stands for Basic Calculator, and it's a command-line utility used for performing arithmetic operations in Unix-based systems. It can handle both integer and floating-point numbers. The `-l` option stands for "math library", and it enables bc to perform operations involving floating-point arithmetic.
```bash
echo "2.5 > 2" | bc -l
1
echo "2.5 < 2" | bc -l
0
echo "2.5 + 2.4" | bc -l
4.9
```

### Text Processing Tools ###

**`awk`** is a powerful text-processing tool used for pattern scanning, data extraction, and reporting in Linux. It works by reading input line by line, splitting it into fields, and applying actions based on conditions.
- $0 → Refers to the entire line.
- $1, $2, ... → Refer to the first, second, etc., fields (columns).
- FS (Field Separator) → Defines how to split columns (default: space/tab).
- ```bash
  #users.txt
  Alice 25
  Bob 30
  ```
  ```bash
  cat users.txt | awk '{ print "User:"$1, "Age:"$2 }'
  ```
  ```bash
  #Output
  User:Alice Age:25
  User:Bob Age:30
  ```
- List all the files of Date *18 Feb*
  ```bash
  ls -lart | awk '$6 == "Feb" && $7 == "18" {print $9}'
  ```
- The `-v` option in `awk` is used to assign values to variables before the `awk` program begins processing the input data
  ```bash
  awk -v var_name=value 'awk_program' input_file
  ```
  ```bash
  awk -v threshold=50 '$1 > threshold {print $0}' data.txt
  ```
  - `$1 > threshold { print $0 }`: This checks if the first column of data.txt is greater than threshold. If it is, the entire line ($0) is printed. 

**`sort`** command in Linux is used to arrange lines of text files in a specified order. By default, it sorts in ascending order (A to Z, 0 to 9), but it can be customized for descending order, numerical sorting, case-insensitive sorting, and more
```bash
sort [OPTIONS] <file>
command | sort [OPTIONS]
```

![image](https://github.com/user-attachments/assets/f53f0242-ef74-42d9-a64e-7a67fb88cdfe)


---

### Variables and User Input ###

- Store a value in a variable and ask for user input.
```bash
#!/bin/bash
name="Alice"
echo "Hello, $name"
echo $name

echo "Enter your Name"
read myName
echo "Hello, $myName"
```

```bash
#Output
Hello, Alice
Alice
Enter your Name
Siddy
Hello, Siddy
```


### For Loop Example ###

- Print numbers from 1 to 5 using a loop.
```bash
#!/bin/bash
for i in {1..5}; do
  echo "Number: $i"
done
```

```bash
#Output
Number 1
Number 2
Number 3
Number 4
Number 5
```

### Functions ###

**Create and call a function.**
```bash
#!/bin/bash
say_hello() {
    echo "Hello, welcome to Bash scripting!"
}

say_hello
```

### Command Line Arguments ###

- Pass arguments to a script and print them.
```bash
#!/bin/bash
echo "First argument: $1"
echo "Second argument: $2"
```

```bash
#Output
/script1.sh Siddharth Singh
First argument: Siddharth
Second argument: Singh
```

### Arrays ###

- Creating a simple list (array):

```bash
#!/bin/bash
my_list=("item1" "item2" "item3" "item4")

echo ${my_list[0]}  # Prints the first element, "item1"
echo ${my_list[1]}  # Prints the second element, "item2"

Iterating over the list:
for item in "${my_list[@]}"; do
    echo "$item"
done
```

- Getting the length of the list:
  ```bash
  length=${#my_list[@]}
  echo "The list has $length elements."
  ```

- Adding elements to the list:
  ```bash
  my_list+=("item5")
  echo ${my_list[@]}  # Now includes "item5"
  ```

**Check if the nginx process is running, start it if it's not, and log the action with a timestamp**

```bash
#!/bin/bash

# Define process name and log file
PROCESS="nginx"
LOG_FILE="/var/log/process_monitor.log"

# Check if the process is running
if ! pgrep -x "$PROCESS" > /dev/null; then
    echo "$(date '+%Y-%m-%d %H:%M:%S') - $PROCESS is not running. Restarting..." >> "$LOG_FILE"
    systemctl start "$PROCESS"
    if [ $? -eq 0 ]; then
        echo "$(date '+%Y-%m-%d %H:%M:%S') - $PROCESS successfully started." >> "$LOG_FILE"
    else
        echo "$(date '+%Y-%m-%d %H:%M:%S') - Failed to start $PROCESS." >> "$LOG_FILE"
    fi
else
    echo "$(date '+%Y-%m-%d %H:%M:%S') - $PROCESS is running." >> "$LOG_FILE"
fi
```
