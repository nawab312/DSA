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
- In awk, `gsub` means global substitution.
  - `gsub(regex, replacement, target)`
  ```bash
  echo "apple apple orange" | awk '{ gsub("apple", "banana"); print }'

  #Output
  banana banana orange
  ```
  - Since no target is specified, it modifies $0 (the whole line).
  ```bash
  echo "id:123:id:456" | awk '{ gsub("id", "user", $1); print $0 }'

  #Output
  echo "id:123:id:456" | awk -F: '{ gsub("id", "user", $1); print $0 }'
  ```
- In awk, `NR` stands for Number of Records. It’s a built-in variable that contains the current input line number, counting across all input files.
  ```bash
  echo -e "a\nb\nc" | awk '{ print NR, $0 }'

  #Output
  1 a
  2 b
  3 c
  ```
  - Only to print 2nd Line
  ```bash
  ls -lart | awk 'NR==2'
  ```
- The `-v` option in `awk` is used to assign values to variables before the `awk` program begins processing the input data
  ```bash
  awk -v var_name=value 'awk_program' input_file
  ```
  ```bash
  awk -v threshold=50 '$1 > threshold {print $0}' data.txt
  ```
  - `$1 > threshold { print $0 }`: This checks if the first column of data.txt is greater than threshold. If it is, the entire line ($0) is printed. 
