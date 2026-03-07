```bash
#!/bin/bash

read -p "Enter the service: " SERVICE_NAME

if systemctl is-active --quiet $SERVICE_NAME; then
    echo "The service '$SERVICE_NAME' is running."
else
    echo "The service '$SERVICE_NAME' is not running, restarting it"
    systemctl restart $SERVICE_NAME
    if [ $? -eq 0 ]; then
        echo "The service '$SERVICE_NAME' has been restarted successfully."
    else
        echo "Failed to restart the service '$SERVICE_NAME'. Please check the service name and try again."
    fi
fi
```

- `$?` is the exit status of the last executed command.
- In Bash, every command returns a numeric code:
  - `0` -> Success
  - Non Zero -> Failure

```bash
#!/bin/bash

# Check if argument is provided
if [ -z "$1" ]; then
    echo "Usage: $0 <service-name>"
    exit 1
fi

SERVICE_NAME=$1
LOG_FILE="/var/log/service_monitor.log"
TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')

if systemctl is-active --quiet "$SERVICE_NAME"; then
    echo "[$TIMESTAMP] $SERVICE_NAME is running OK" | tee -a "$LOG_FILE"
else
    echo "[$TIMESTAMP] $SERVICE_NAME was DOWN - attempting restart..." | tee -a "$LOG_FILE"
    
    systemctl restart "$SERVICE_NAME"
    
    if [ $? -eq 0 ]; then
        echo "[$TIMESTAMP] $SERVICE_NAME was DOWN - restarted successfully" | tee -a "$LOG_FILE"
    else
        echo "[$TIMESTAMP] $SERVICE_NAME was DOWN - restart FAILED" | tee -a "$LOG_FILE"
        exit 1
    fi
fi
```
