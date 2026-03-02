```bash
#!/bin/bash

FILE=$1

if [ ! -f $FILE ]; then
    echo "File $FILE does not exist"
    exit 1
fi

tr '[:upper:]' '[:lower:]' < $FILE \
    | sed 's/[^a-z0-9]/ /g' \
    | tr -s ' ' '\n' \
    | sort \
    | uniq -c \
    | sort -nr \
    | head -5
```
