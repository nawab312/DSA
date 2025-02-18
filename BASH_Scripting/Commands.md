Find files by Date and Copy them to /tmp/ folder
```bash
ls -lart | awk '$6 == "Feb" && $7 == "18" {print $9}' | xargs -I {} cp {} /tmp/
```
