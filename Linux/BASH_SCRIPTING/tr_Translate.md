- `tr` (translate) is a Unix command that reads from standard input and performs character-by-character transformations on the stream.
- It does not understand: words, fields, lines, regex
- It only maps or removes characters.

**Core Capabilities**

- Character Translation: Replace one set of characters with another.
  ```bash
  echo "ABC" | tr 'ABC' 'xyz'

  #Output
  xyz
  ```
  - It maps positionally: A → x, B → y, C → z
- Character Deletion (-d): Remove characters completely.
  ```bash
  echo "hello123" | tr -d '0-9'

  #Output
  hello
  ```
- Squeezing Repeated Characters (-s): Collapse repeated characters into one.
  ```bash
  echo "hello     world" | tr -s ' '

  #Output
  hello world
  ```

  ```bash
  tr -s ' ' '\n'
  ```
  - Replace every space ' ' with newline '\n'
  - Then squeeze repeated newlines into a single newline.
  - Example:
    - Input: `hello     world   test`
    - Step 1 (space → newline):
      ```bash
      hello



      world


      test
      ```
    - Step 2 (squeeze repeated newlines):
      ```bash
      hello
      world
      test
      ```
- Conver Upper to Lower
  ```bash
  echo "HELLO World" | tr '[:upper:]' '[:lower:]'

  #Output
  hello world
  ```
  
