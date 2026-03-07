**Check disk space usage of file systems**
```bash
df -h

Filesystem      Size  Used Avail Use% Mounted on
/dev/sda1       100G   70G   25G  75% /
```
- df → “disk filesystem”
- -h → human-readable (GB, MB)
- df shows usage per filesystem, not per directory. Large files in subdirectories might be hidden.

**Check disk usage of directories**
```bash
du -sh /var/log

Output: 2.1G   /var/log
```
- -s → summarize (don’t list every file)
- To see detailed sizes of subdirectories:
  ```bash
  du -sh --max-depth=1 /var
  ```
- This lists top 10 largest directories/files.
  ```bash
  du -sh /var | sort -h | tail -n 10
  ```

**Check inode usage**
- Sometimes disk is full but df shows space available because of inodes. Shows inode usage per filesystem.
```bash
df -i
```

**Monitor disk usage in real-time**
```bash
watch -n 5 df -h
```

**Monitor disk usage in real-time**
- `ncdu` → interactive disk usage analyzer. Lets you navigate directories and see what’s taking space.
```bash
sudo apt install ncdu   # Debian/Ubuntu
sudo yum install ncdu   # RHEL/CentOS
ncdu /
```

---

You run `df -h` on a Linux server and the disk is 100% full. How do you find which directory or file is consuming the most space?
```bash
# Step 1 — check which partition is full
df -h

# Step 2 — find largest directories from root
du -sh /* | sort -h | tail -n 20

# Step 3 — drill down into the biggest directory
du -sh /var/* | sort -h | tail -n 20
```

---

  
