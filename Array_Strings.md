### Longest Substring Without Repeating Characters

Given a string s, find the length of the longest substring without duplicate characters.
```
Example 1:

Input: s = "abcabcbb"
Output: 3
Explanation: The answer is "abc", with the length of 3. Note that "bca" and "cab" are also correct answers.
```

```
Example 2:

Input: s = "bbbbb"
Output: 1
Explanation: The answer is "b", with the length of 1.
```

```
Example 3:

Input: s = "pwwkew"
Output: 3
Explanation: The answer is "wke", with the length of 3.
Notice that the answer must be a substring, "pwke" is a subsequence and not a substring.
```

It uses a *variable-size sliding window* combined with a *Hash Set/Map* for O(1) 

- Maintain a window `[left, right]` where all characters are unique
- Expand `right`, and when a duplicate is found, shrink from `left` until the duplicate is removed.

```python
def lengthOfLongestSubstring(s: str) -> int:
    char_set = set()
    left = 0
    max_len = 0

    for right in range(len(s)):
        while s[right] in char_set:
            char_set.remove(s[left])
            left += 1
        char_set.add(s[right])
        max_len = max(max_len, right - left + 1)

    return max_len
```

Complexity: Time `O(n)`, Space `O(min(n, m))` where m = charset size

Why Space Comlexity `O(min(n, m))`
- At any moment, the set contains: only unique characters
  - Example: `"abcdef"`
  - Set grows like: `{a, b, c, d, e, f} -> size = n`
  - Space = O(n)
- Limited character set
  - Example: `"abcabcbb"`
  - Even if string is long, characters are only: `{a, b, c}`
  - Space = O(m) (where m = `charset size`)
 
Optimized variant using a `HashMap` to jump left directly instead of crawling:
```python
def lengthOfLongestSubstring(s: str) -> int:
    char_index = {}
    left = 0
    max_len = 0

    for right, char in enumerate(s):
        if char in char_index and char_index[char] >= left:
            left = char_index[char] + 1
        char_index[char] = right
        max_len = max(max_len, right - left + 1)

    return max_len
```

---
