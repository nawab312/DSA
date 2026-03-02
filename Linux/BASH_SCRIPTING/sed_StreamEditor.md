- It reads input line by line, applies editing commands, and prints the result to stdout.
- It does not load the whole file into memory.
- It processes text as a stream.

**Substitution**

```bash
sed 's/pattern/replacement/'
```

```bash
echo "apple orange apple" | sed 's/apple/banana/'

#Output
banana orange apple
```
- Only the first match per line is replaced. To replace all:
  ```bash
  sed 's/apple/banana/g'
  ```

**Line Selection**
- Prints line 2 (but also prints everything unless you suppress default output). So it will print every line (default behavior). Print line 2 again because of `p`
  ```bash
  sed '2p' file
  ```
- If you want to suppress the default printing. Only lines explicitly told to print (`p`) are printed
  ```bash
  sed -n '2p' file
  ```

**Delete Lines**
- Deletes lines matching "error".
  ```bash
  sed '/error/d`
  ```

**In-Place Editing**
- Modifies the file directly. Be careful this changes the file permanently.
  ```bash
  sed -i 's/foo/bar/g' file.txt
  ```
  
