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
