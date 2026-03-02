- uniq removes adjacent duplicate lines from input. Key word: *adjacent*.
- It does not remove all duplicates globally unless the input is sorted first.

```bash
echo -e "a\na\nb\na" | uniq

#Output
a
b
a
```
- Notice the last a is still there. Because it was not next to the first a.

**Why People Use sort | uniq**

```bash
sort file | uniq
```
- sort groups identical lines together.
- Then uniq removes the duplicates.
- Without sorting, uniq is often wrong.

**Common Flags**
- -c → Count occurrences
  ```bash
  echo -e "a\na\nb" | sort | uniq -c

  #Output
  2 a
  1 b
  ```
- -d → Only show duplicates. Shows lines that appear more than once.
  ```bash
  uniq -d
  ```
- -u → Only show unique lines. Shows lines that appear exactly once.

  
  
