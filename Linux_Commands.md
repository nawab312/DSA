Command to check which process is using port 5432:
```bash
sudo lsof -i :5432
```
Create a new user called username, set their shell to /bin/bash, and create their home directory.
```bash
sudo useradd -m -s /bin/bash username
```
List Partitions: To list the available disk partitions on your system, run
```bash
sudo fdisk -l
```
