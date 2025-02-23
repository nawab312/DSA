Command to check which process is using port 5432:
```bash
sudo lsof -i :5432
```
<br><br>
Create a new user called username, set their shell to /bin/bash, and create their home directory.
```bash
sudo useradd -m -s /bin/bash username
```
