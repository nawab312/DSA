```bash
#!/bin/bash

THRESHOLD=80
DISK_USAGE=$(df -h / | awk 'NR==2 {gsub("%", ""); print $5}')

if [ -z $DISK_USAGE ]; then
    echo "Error: Unable to retrieve disk usage."
    exit 2
fi

if [ $DISK_USAGE -gt $THRESHOLD ]; then
    echo "Warning: Disk usage is at ${DISK_USAGE}%, which exceeds the threshold of ${THRESHOLD}%."
else
    echo "Disk usage is at ${DISK_USAGE}%, which is within the acceptable range."
fi
```
