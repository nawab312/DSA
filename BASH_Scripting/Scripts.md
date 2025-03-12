**`xargs`** is a command in Linux that allows you to take standard input (stdin) and convert it into command-line arguments for another command. It's useful for handling large lists of arguments that might exceed the shell's command-line length limit.
- ```bash
  echo "file1 file2 file3" | xargs rm
  ```
  This deletes file1, file2, and file3 by passing them as arguments to rm.
- ```bash
  ls | xargs -n 2 echo
  ```
  ```bash
  #Output
  script1.sh script2.sh
  script3.sh script4.sh
  script5.sh
  ```
  Processes two filenames at a time.


### Variables and User Input ###

**Store a value in a variable and ask for user input.**
```bash
#!/bin/bash
name="Alice"
echo "Hello, $name"
echo $name

echo "Enter your Name"
read myName
echo "Hello, $myName"
```

```bash
#Output
Hello, Alice
Alice
Enter your Name
Siddy
Hello, Siddy
```

### If-Else ###

**Check if a number is positive or negative.**
```bash
#!/bin/bash
echo "Enter a Number"
read num

if [ $num -gt 0 ]; then
  echo "$num is Positive Number"
elif [ $num -lt 0 ]; then
  echo "$num is Negative Number"
else
  echo "$num is Zero"
fi
```

```bash
#Output
Enter a Number
11
11 is Positive Number
```

**Check If a File Exists**
- `-f` checks if the given file exists and is a regular file.

```bash
#!/bin/bash
echo "Enter the file Name"
read file

if [ -f $file ]; then
  echo "File Exists"
else 
  echo "File doesnt Exists"
fi
```

```bash
#Output
Enter the file Name
script1.sh
File Exists

Enter the file Name
script3.sh
File doesnt Exists
```

### For Loop Example ###

**Print numbers from 1 to 5 using a loop.**
```bash
#!/bin/bash
for i in {1..5}; do
  echo "Number: $i"
done
```

```bash
#Output
Number 1
Number 2
Number 3
Number 4
Number 5
```

### Functions ###

**Create and call a function.**
```bash
#!/bin/bash
say_hello() {
    echo "Hello, welcome to Bash scripting!"
}

say_hello
```

### Command Line Arguments ###

**Pass arguments to a script and print them.**
```bash
#!/bin/bash
echo "First argument: $1"
echo "Second argument: $2"
```

```bash
#Output
/script1.sh Siddharth Singh
First argument: Siddharth
Second argument: Singh
```
