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
