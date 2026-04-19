# Hashmaps — Complete MAANG Interview Guide
## Frequency counting, Grouping, Lookup optimization

> **Target:** Recognize when a hashmap turns O(n²) into O(n). Use hashmaps instinctively in every interview.
> **Why this matters:** Hashmaps are the single most useful data structure in coding interviews. They solve more problems than any other structure. If you're stuck on any problem, your first thought should be "can a hashmap help here?"

---

## Table of contents

1. [How hashmaps work internally](#1-how-hashmaps-work-internally)
2. [Python dict/set fundamentals](#2-python-dictset-fundamentals)
3. [Pattern 1: Lookup optimization (O(n²) → O(n))](#3-pattern-1-lookup-optimization)
4. [Pattern 2: Frequency counting](#4-pattern-2-frequency-counting)
5. [Pattern 3: Grouping / bucketing](#5-pattern-3-grouping--bucketing)
6. [Pattern 4: Two-pass hashmap](#6-pattern-4-two-pass-hashmap)
7. [Pattern 5: Hashmap + sliding window](#7-pattern-5-hashmap--sliding-window)
8. [Pattern 6: Hashmap + prefix sum](#8-pattern-6-hashmap--prefix-sum)
9. [Pattern 7: Index tracking](#9-pattern-7-index-tracking)
10. [Pattern 8: Caching / memoization](#10-pattern-8-caching--memoization)
11. [Infra-relevant hashmap problems](#11-infra-relevant-hashmap-problems)
12. [LeetCode problem list (25 problems)](#12-leetcode-problem-list-25-problems)
13. [Interview tips for hashmap problems](#13-interview-tips-for-hashmap-problems)
14. [Common mistakes](#14-common-mistakes)
15. [Cheat sheet](#15-cheat-sheet)

---

## 1. How hashmaps work internally

Interviewers sometimes ask this. Know it at a conceptual level.

### The basics

A hashmap stores key-value pairs. Under the hood:

1. **Hash function** takes the key and computes an integer (the hash)
2. That integer maps to a **bucket** (an index in an internal array)
3. The value is stored in that bucket

```
key "alice" → hash("alice") = 394821 → bucket 394821 % 16 = 5 → store at index 5
```

### Hash collisions

Two different keys can hash to the same bucket. This is called a **collision**.

**Chaining** (Python's approach): Each bucket holds a linked list. Colliding keys are appended to the list. Lookup walks the list to find the right key.

**Open addressing**: If the bucket is taken, probe the next bucket (linear probing, quadratic probing, or double hashing).

### Time complexity

| Operation | Average | Worst case |
|-----------|---------|------------|
| Insert | O(1) | O(n) — all keys collide |
| Lookup | O(1) | O(n) — all keys collide |
| Delete | O(1) | O(n) — all keys collide |

Worst case is theoretical — with a good hash function (Python's built-in is excellent), you'll never hit it in practice. **Always state O(1) for hashmap operations in interviews.**

### What can be a hashmap key?

The key must be **hashable** — immutable and has a consistent hash value.

```python
# Valid keys (hashable)
d[42] = "int"              # integers
d["hello"] = "string"      # strings
d[(1, 2)] = "tuple"        # tuples (of hashable elements)
d[True] = "bool"           # booleans
d[frozenset({1,2})] = "fs" # frozensets

# INVALID keys (unhashable) — will raise TypeError
d[[1, 2]] = "list"         # lists are mutable
d[{1, 2}] = "set"          # sets are mutable
d[{"a": 1}] = "dict"       # dicts are mutable
```

**Interview tip:** If you need a list as a key, convert it to a tuple first.

```python
# Grouping anagrams — need sorted characters as key
key = tuple(sorted("eat"))  # ('a', 'e', 't') — hashable
```

---

## 2. Python dict/set fundamentals

### dict — key-value pairs

```python
# Creating
d = {}                          # empty dict
d = {"a": 1, "b": 2}           # literal
d = dict(a=1, b=2)             # keyword args
d = {x: x**2 for x in range(5)} # comprehension

# Basic operations — ALL O(1)
d["key"] = value                # insert/update
value = d["key"]                # lookup (raises KeyError if missing)
value = d.get("key", default)   # lookup with default (no error)
"key" in d                      # existence check
del d["key"]                    # delete
len(d)                          # count of key-value pairs

# Iteration — O(n)
for key in d:                   # iterate keys
for key, value in d.items():    # iterate pairs
for value in d.values():        # iterate values

# Useful methods
d.get(key, 0)                   # returns 0 if key missing (not KeyError)
d.setdefault(key, [])           # if key missing, set to [] and return it
d.pop(key, None)                # remove and return, None if missing
d.update(other_dict)            # merge other_dict into d
```

### defaultdict — dict that auto-creates missing keys

```python
from collections import defaultdict

# Instead of checking "if key in dict" before accessing:
d = defaultdict(list)           # missing key → empty list
d["fruits"].append("apple")    # no KeyError! auto-creates the list
d["fruits"].append("banana")
# d = {"fruits": ["apple", "banana"]}

d = defaultdict(int)            # missing key → 0
d["count"] += 1                 # no KeyError! starts at 0
# d = {"count": 1}

d = defaultdict(set)            # missing key → empty set
d["users"].add("alice")
```

**When to use:** Any time you'd write `if key not in d: d[key] = []` before appending. defaultdict eliminates that boilerplate.

### Counter — specialized dict for counting

```python
from collections import Counter

# Count frequencies
freq = Counter([1, 2, 2, 3, 3, 3])
# Counter({3: 3, 2: 2, 1: 1})

freq = Counter("abracadabra")
# Counter({'a': 5, 'b': 2, 'r': 2, 'c': 1, 'd': 1})

# Useful methods
freq.most_common(2)             # [(3, 3), (2, 2)] — top 2
freq[99]                        # 0 (missing keys return 0, not KeyError)
freq.total()                    # sum of all counts (Python 3.10+)

# Counter arithmetic
c1 = Counter("aab")             # {'a': 2, 'b': 1}
c2 = Counter("abb")             # {'a': 1, 'b': 2}
c1 - c2                         # Counter({'a': 1}) — only positive counts
c1 & c2                         # Counter({'a': 1, 'b': 1}) — min of each
c1 | c2                         # Counter({'a': 2, 'b': 2}) — max of each

# Check if one Counter is subset of another
# (useful for anagram/permutation checking)
def is_subset(c1, c2):
    return all(c1[k] <= c2[k] for k in c1)
```

### set — hashmap with keys only (no values)

```python
# Creating
s = set()                       # empty set (NOT {}, that's a dict)
s = {1, 2, 3}                  # literal
s = set([1, 2, 2, 3])          # from list, auto-deduplicates → {1, 2, 3}

# Operations — ALL O(1)
s.add(4)                        # insert
s.remove(4)                     # remove (raises KeyError if missing)
s.discard(4)                    # remove (no error if missing)
4 in s                          # existence check
len(s)                          # count

# Set operations — O(min(len(a), len(b)))
a | b                           # union
a & b                           # intersection
a - b                           # difference (in a but not in b)
a ^ b                           # symmetric difference (in a or b but not both)
a <= b                          # is a subset of b?
a >= b                          # is a superset of b?
```

**The key insight:** `x in list` is O(n). `x in set` is O(1). Converting a list to a set before lookups is one of the most common optimizations in interviews.

---

## 3. Pattern 1: Lookup optimization

### The core idea

Replace an inner loop with a hashmap lookup. This turns O(n²) into O(n).

**Before (O(n²)):** For each element, scan the entire array to find a match.
**After (O(n)):** For each element, check the hashmap in O(1).

### Problem: Two Sum (LC #1, Easy) — THE most famous interview problem

Given an array and a target, find two numbers that add up to target. Return indices.

```python
# Brute force — O(n²)
def two_sum_brute(nums, target):
    for i in range(len(nums)):
        for j in range(i + 1, len(nums)):
            if nums[i] + nums[j] == target:
                return [i, j]
    return []

# Hashmap — O(n)
def two_sum(nums, target):
    seen = {}  # value → index
    
    for i, num in enumerate(nums):
        complement = target - num
        
        if complement in seen:
            return [seen[complement], i]
        
        seen[num] = i
    
    return []
```

Walk through with `nums = [2, 7, 11, 15], target = 9`:

```
i=0, num=2:  complement = 9-2 = 7,  7 not in seen,  store {2: 0}
i=1, num=7:  complement = 9-7 = 2,  2 IS in seen!   return [0, 1]
```

**The mental model:** For each number, ask "have I already seen the number that would complete this pair?" The hashmap remembers everything you've seen so far.

**Time: O(n), Space: O(n)**

### Problem: Two Sum — finding all pairs (infra variant)

```python
def find_all_pairs(nums, target):
    """Find all unique pairs that sum to target"""
    seen = set()
    used = set()
    result = []
    
    for num in nums:
        complement = target - num
        if complement in seen and (min(num, complement), max(num, complement)) not in used:
            pair = (min(num, complement), max(num, complement))
            result.append(pair)
            used.add(pair)
        seen.add(num)
    
    return result
```

### Problem: Contains Duplicate (LC #217, Easy)

```python
def contains_duplicate(nums):
    seen = set()
    for num in nums:
        if num in seen:
            return True
        seen.add(num)
    return False

# Even shorter:
def contains_duplicate(nums):
    return len(nums) != len(set(nums))
```

### Problem: Intersection of Two Arrays (LC #349, Easy)

```python
def intersection(nums1, nums2):
    return list(set(nums1) & set(nums2))
```

### Problem: Longest Consecutive Sequence (LC #128, Medium) — very common

Find the length of the longest consecutive sequence. Must be O(n).

You can't sort (that's O(n log n)). Use a set for O(1) lookups.

```python
def longest_consecutive(nums):
    num_set = set(nums)
    best = 0
    
    for num in num_set:
        # Only start counting from the beginning of a sequence
        if num - 1 not in num_set:
            current = num
            streak = 1
            
            while current + 1 in num_set:
                current += 1
                streak += 1
            
            best = max(best, streak)
    
    return best

# Example: [100, 4, 200, 1, 3, 2]
# num_set = {1, 2, 3, 4, 100, 200}
#
# num=1: 1-1=0 not in set → start of sequence
#        1→2→3→4 → streak = 4
# num=2: 2-1=1 IS in set → skip (not start of sequence)
# num=3: 3-1=2 IS in set → skip
# num=4: 4-1=3 IS in set → skip
# num=100: 100-1=99 not in set → start, streak = 1
# num=200: 200-1=199 not in set → start, streak = 1
#
# Answer: 4
```

**The trick:** Only start counting from numbers that are the START of a sequence (i.e., `num - 1` is not in the set). This ensures each number is visited at most twice — O(n) total.

### Problem: Valid Sudoku (LC #36, Medium)

Use sets to track seen numbers in each row, column, and 3x3 box.

```python
def is_valid_sudoku(board):
    rows = defaultdict(set)
    cols = defaultdict(set)
    boxes = defaultdict(set)
    
    for r in range(9):
        for c in range(9):
            val = board[r][c]
            if val == '.':
                continue
            
            box_id = (r // 3, c // 3)
            
            if val in rows[r] or val in cols[c] or val in boxes[box_id]:
                return False
            
            rows[r].add(val)
            cols[c].add(val)
            boxes[box_id].add(val)
    
    return True
```

---

## 4. Pattern 2: Frequency counting

### The core idea

Count how many times each element appears. Then use those counts to answer the question.

### Problem: Valid Anagram (LC #242, Easy)

Two strings are anagrams if they have the same character frequencies.

```python
def is_anagram(s, t):
    return Counter(s) == Counter(t)

# Manual version (interviewers might ask you to implement without Counter):
def is_anagram_manual(s, t):
    if len(s) != len(t):
        return False
    
    count = {}
    for char in s:
        count[char] = count.get(char, 0) + 1
    
    for char in t:
        if char not in count or count[char] == 0:
            return False
        count[char] -= 1
    
    return True
```

### Problem: Top K Frequent Elements (LC #347, Medium)

```python
# Approach 1: Counter.most_common — O(n log n)
def top_k(nums, k):
    return [x for x, _ in Counter(nums).most_common(k)]

# Approach 2: Bucket sort — O(n) ← optimal
def top_k_optimal(nums, k):
    freq = Counter(nums)
    
    # Bucket sort: index = frequency, value = list of elements
    # Max possible frequency = len(nums)
    buckets = [[] for _ in range(len(nums) + 1)]
    for num, count in freq.items():
        buckets[count].append(num)
    
    # Collect from highest frequency buckets
    result = []
    for i in range(len(buckets) - 1, -1, -1):
        for num in buckets[i]:
            result.append(num)
            if len(result) == k:
                return result
    
    return result

# Example: nums = [1,1,1,2,2,3], k = 2
# freq = {1:3, 2:2, 3:1}
# buckets[1] = [3], buckets[2] = [2], buckets[3] = [1]
# Scan from right: buckets[3]=[1] → result=[1]
#                  buckets[2]=[2] → result=[1,2] → done
# Answer: [1, 2]
```

**Why bucket sort works here:** The maximum possible frequency is n (all elements are the same). So we create n+1 buckets, place each element in its frequency bucket, and scan from the highest bucket. No comparison-based sorting needed.

### Problem: Sort Characters By Frequency (LC #451, Medium)

```python
def frequency_sort(s):
    freq = Counter(s)
    # Sort characters by frequency (descending)
    sorted_chars = sorted(freq.keys(), key=lambda c: -freq[c])
    return "".join(c * freq[c] for c in sorted_chars)

# "tree" → freq = {'t':1, 'r':1, 'e':2}
# sorted by freq: ['e', 't', 'r'] (or ['e', 'r', 't'])
# result: "eert" (or "eetr")
```

### Problem: First Unique Character in a String (LC #387, Easy)

```python
def first_uniq_char(s):
    freq = Counter(s)
    
    for i, char in enumerate(s):
        if freq[char] == 1:
            return i
    
    return -1

# "leetcode" → freq = {l:1, e:3, t:1, c:1, o:1, d:1}
# First char with count 1: 'l' at index 0
```

### Problem: Majority Element (LC #169, Easy)

Element that appears more than n/2 times.

```python
# Hashmap approach — O(n) time, O(n) space
def majority_element(nums):
    freq = Counter(nums)
    return max(freq.keys(), key=freq.get)

# Boyer-Moore voting — O(n) time, O(1) space (optimal)
def majority_element_optimal(nums):
    candidate = None
    count = 0
    
    for num in nums:
        if count == 0:
            candidate = num
        count += 1 if num == candidate else -1
    
    return candidate

# Why Boyer-Moore works:
# The majority element appears MORE than n/2 times.
# Every time we "cancel" a pair of different elements,
# the majority element still has more copies remaining.
# The last standing candidate is guaranteed to be the majority.
```

### Problem: Minimum Window to make strings equal frequency

```python
def min_deletions_to_make_freq_unique(s):
    """LC #1647 — make all character frequencies unique"""
    freq = Counter(s)
    used = set()
    deletions = 0
    
    for char, count in freq.items():
        while count > 0 and count in used:
            count -= 1
            deletions += 1
        if count > 0:
            used.add(count)
    
    return deletions
```

---

## 5. Pattern 3: Grouping / bucketing

### The core idea

Group elements by some computed key. Elements with the same key belong together.

### Problem: Group Anagrams (LC #49, Medium) — asked very frequently

```python
def group_anagrams(strs):
    groups = defaultdict(list)
    
    for s in strs:
        key = tuple(sorted(s))  # anagrams have the same sorted form
        groups[key].append(s)
    
    return list(groups.values())

# ["eat", "tea", "tan", "ate", "nat", "bat"]
#
# key ('a','e','t') → ["eat", "tea", "ate"]
# key ('a','n','t') → ["tan", "nat"]
# key ('a','b','t') → ["bat"]
```

**Time: O(n * k log k)** where n is number of strings and k is max string length (sorting each string).

**Optimization — use character count as key instead of sorting:**

```python
def group_anagrams_optimal(strs):
    groups = defaultdict(list)
    
    for s in strs:
        # Count of each character (26 lowercase letters)
        count = [0] * 26
        for c in s:
            count[ord(c) - ord('a')] += 1
        key = tuple(count)  # (1, 0, 0, ..., 1, ..., 1) — hashable
        groups[key].append(s)
    
    return list(groups.values())
```

**Time: O(n * k)** — no sorting needed. Each string is processed in O(k).

### Problem: Group people by age range

```python
def group_by_age_range(people):
    """Group list of (name, age) by decade"""
    groups = defaultdict(list)
    
    for name, age in people:
        decade = (age // 10) * 10  # 23 → 20, 35 → 30
        groups[decade].append(name)
    
    return dict(groups)

# [("Alice", 23), ("Bob", 35), ("Charlie", 28), ("Diana", 31)]
# → {20: ["Alice", "Charlie"], 30: ["Bob", "Diana"]}
```

### Problem: Group logs by error type (infra-relevant)

```python
def group_errors(log_lines):
    """Group log lines by error type"""
    groups = defaultdict(list)
    
    for line in log_lines:
        if "ERROR" in line:
            # Extract error type: everything after "ERROR"
            error_type = line.split("ERROR")[1].strip().split(":")[0].strip()
            groups[error_type].append(line)
    
    return dict(groups)
```

### Problem: Encode and Decode TinyURL (LC #535, Medium)

```python
class Codec:
    def __init__(self):
        self.url_to_code = {}
        self.code_to_url = {}
        self.counter = 0
    
    def encode(self, longUrl):
        if longUrl in self.url_to_code:
            return self.url_to_code[longUrl]
        
        self.counter += 1
        code = f"http://tiny.url/{self.counter}"
        self.url_to_code[longUrl] = code
        self.code_to_url[code] = longUrl
        return code
    
    def decode(self, shortUrl):
        return self.code_to_url.get(shortUrl, "")
```

### Problem: Isomorphic Strings (LC #205, Easy)

Two strings where characters can be mapped 1:1.

```python
def is_isomorphic(s, t):
    if len(s) != len(t):
        return False
    
    s_to_t = {}
    t_to_s = {}
    
    for cs, ct in zip(s, t):
        if cs in s_to_t:
            if s_to_t[cs] != ct:
                return False
        else:
            s_to_t[cs] = ct
        
        if ct in t_to_s:
            if t_to_s[ct] != cs:
                return False
        else:
            t_to_s[ct] = cs
    
    return True

# "egg" and "add" → e→a, g→d → True
# "foo" and "bar" → f→b, o→a, o→r (conflict: o maps to both a and r) → False
```

### Problem: Word Pattern (LC #290, Easy)

```python
def word_pattern(pattern, s):
    words = s.split()
    if len(pattern) != len(words):
        return False
    
    char_to_word = {}
    word_to_char = {}
    
    for c, w in zip(pattern, words):
        if c in char_to_word and char_to_word[c] != w:
            return False
        if w in word_to_char and word_to_char[w] != c:
            return False
        char_to_word[c] = w
        word_to_char[w] = c
    
    return True

# pattern = "abba", s = "dog cat cat dog" → True
# a→dog, b→cat, b→cat(✓), a→dog(✓)
```

---

## 6. Pattern 4: Two-pass hashmap

### The core idea

First pass: build the hashmap. Second pass: use it to answer questions.

### Problem: First Unique Character (already shown above)

Pass 1: count frequencies. Pass 2: find first with count 1.

### Problem: Find All Duplicates in an Array (LC #442, Medium)

```python
def find_duplicates(nums):
    # Using hashmap — O(n) time, O(n) space
    freq = Counter(nums)
    return [num for num, count in freq.items() if count == 2]

# Follow-up: O(1) space? Use array as hashmap (mark visited by negating)
def find_duplicates_optimal(nums):
    result = []
    for num in nums:
        idx = abs(num) - 1
        if nums[idx] < 0:
            result.append(abs(num))
        else:
            nums[idx] = -nums[idx]
    return result
```

### Problem: Ransom Note (LC #383, Easy)

Can you construct `ransomNote` from letters in `magazine`?

```python
def can_construct(ransomNote, magazine):
    available = Counter(magazine)
    
    for char in ransomNote:
        if available[char] <= 0:
            return False
        available[char] -= 1
    
    return True

# Shorter:
def can_construct(ransomNote, magazine):
    return not (Counter(ransomNote) - Counter(magazine))
```

---

## 7. Pattern 5: Hashmap + sliding window

### The core idea

Use a hashmap to track the state of a sliding window. The hashmap stores character counts, element frequencies, or other window properties.

### Problem: Permutation in String (LC #567, Medium)

Check if s2 contains a permutation of s1.

```python
def check_inclusion(s1, s2):
    if len(s1) > len(s2):
        return False
    
    need = Counter(s1)
    window = Counter(s2[:len(s1)])
    
    if window == need:
        return True
    
    for i in range(len(s1), len(s2)):
        # Add new character on right
        window[s2[i]] += 1
        
        # Remove old character on left
        old = s2[i - len(s1)]
        window[old] -= 1
        if window[old] == 0:
            del window[old]
        
        if window == need:
            return True
    
    return False

# s1 = "ab", s2 = "eidbaooo"
# Window size = 2
# "ei" → no, "id" → no, "db" → no, "ba" → Counter matches "ab" → True
```

**Optimization — avoid comparing entire Counters each step:**

```python
def check_inclusion_optimized(s1, s2):
    if len(s1) > len(s2):
        return False
    
    need = Counter(s1)
    window = Counter()
    matches = 0                    # how many chars have correct count
    required = len(need)           # how many unique chars need matching
    
    for i in range(len(s2)):
        # Add right character
        char = s2[i]
        window[char] += 1
        if char in need and window[char] == need[char]:
            matches += 1
        elif char in need and window[char] == need[char] + 1:
            matches -= 1           # was matching, now over-count
        
        # Remove left character (when window exceeds s1 length)
        if i >= len(s1):
            left_char = s2[i - len(s1)]
            if left_char in need and window[left_char] == need[left_char]:
                matches -= 1       # was matching, now removing
            elif left_char in need and window[left_char] == need[left_char] + 1:
                matches += 1       # was over-count, now correct
            window[left_char] -= 1
        
        if matches == required:
            return True
    
    return False
```

### Problem: Find All Anagrams in a String (LC #438, Medium)

Return starting indices of all anagram windows.

```python
def find_anagrams(s, p):
    if len(p) > len(s):
        return []
    
    need = Counter(p)
    window = Counter(s[:len(p)])
    result = []
    
    if window == need:
        result.append(0)
    
    for i in range(len(p), len(s)):
        window[s[i]] += 1
        
        old = s[i - len(p)]
        window[old] -= 1
        if window[old] == 0:
            del window[old]
        
        if window == need:
            result.append(i - len(p) + 1)
    
    return result
```

### Problem: Longest Substring with At Most K Distinct (uses hashmap to track window)

```python
def longest_k_distinct(s, k):
    count = {}    # char → frequency in current window
    left = 0
    best = 0
    
    for right in range(len(s)):
        count[s[right]] = count.get(s[right], 0) + 1
        
        while len(count) > k:
            count[s[left]] -= 1
            if count[s[left]] == 0:
                del count[s[left]]
            left += 1
        
        best = max(best, right - left + 1)
    
    return best
```

---

## 8. Pattern 6: Hashmap + prefix sum

### The core idea

Store prefix sums in a hashmap to find subarrays with a target sum in O(n).

This was covered in the arrays guide but it's fundamentally a hashmap pattern.

### Problem: Subarray Sum Equals K (LC #560, Medium)

```python
def subarray_sum(nums, k):
    count = 0
    prefix = 0
    seen = {0: 1}    # prefix_sum → number of times seen
    
    for num in nums:
        prefix += num
        
        if prefix - k in seen:
            count += seen[prefix - k]
        
        seen[prefix] = seen.get(prefix, 0) + 1
    
    return count
```

### Problem: Continuous Subarray Sum (LC #523, Medium)

Check if there's a subarray of length >= 2 with sum that's a multiple of k.

```python
def check_subarray_sum(nums, k):
    remainder_index = {0: -1}    # remainder → first index
    prefix = 0
    
    for i in range(len(nums)):
        prefix += nums[i]
        remainder = prefix % k
        
        if remainder in remainder_index:
            if i - remainder_index[remainder] >= 2:
                return True
        else:
            remainder_index[remainder] = i
    
    return False

# Key insight: if prefix[j] % k == prefix[i] % k,
# then (prefix[j] - prefix[i]) % k == 0,
# meaning the subarray between i and j sums to a multiple of k.
```

---

## 9. Pattern 7: Index tracking

### The core idea

Use hashmap to remember where you last saw something. Useful for "nearest" or "distance" problems.

### Problem: Contains Duplicate II (LC #219, Easy)

Check if there are duplicates within distance k.

```python
def contains_nearby_duplicate(nums, k):
    last_seen = {}    # value → last index
    
    for i, num in enumerate(nums):
        if num in last_seen and i - last_seen[num] <= k:
            return True
        last_seen[num] = i
    
    return False
```

### Problem: Shortest Word Distance (LC #243, Easy)

```python
def shortest_distance(words, word1, word2):
    last1 = last2 = -1
    best = float('inf')
    
    for i, word in enumerate(words):
        if word == word1:
            last1 = i
        elif word == word2:
            last2 = i
        
        if last1 != -1 and last2 != -1:
            best = min(best, abs(last1 - last2))
    
    return best
```

### Problem: Bulls and Cows (LC #299, Medium)

```python
def get_hint(secret, guess):
    bulls = 0
    s_count = Counter()
    g_count = Counter()
    
    for s, g in zip(secret, guess):
        if s == g:
            bulls += 1
        else:
            s_count[s] += 1
            g_count[g] += 1
    
    # Cows: characters that match but in wrong position
    cows = sum((s_count & g_count).values())
    
    return f"{bulls}A{cows}B"
```

---

## 10. Pattern 8: Caching / memoization

### The core idea

Store computed results in a hashmap to avoid recalculating. This is the foundation of dynamic programming.

### Problem: Climbing Stairs with memoization

```python
def climb_stairs(n):
    memo = {}
    
    def dp(i):
        if i <= 1:
            return 1
        if i in memo:
            return memo[i]
        
        memo[i] = dp(i - 1) + dp(i - 2)
        return memo[i]
    
    return dp(n)

# Without memo: O(2^n) — exponential
# With memo: O(n) — each subproblem solved once
```

### Using @lru_cache (Python's built-in memoization)

```python
from functools import lru_cache

def climb_stairs(n):
    @lru_cache(maxsize=None)
    def dp(i):
        if i <= 1:
            return 1
        return dp(i - 1) + dp(i - 2)
    
    return dp(n)

# lru_cache stores results automatically — no manual dict needed
```

### Problem: Word Break (LC #139, Medium)

```python
def word_break(s, wordDict):
    word_set = set(wordDict)
    memo = {}
    
    def dp(start):
        if start == len(s):
            return True
        if start in memo:
            return memo[start]
        
        for end in range(start + 1, len(s) + 1):
            if s[start:end] in word_set and dp(end):
                memo[start] = True
                return True
        
        memo[start] = False
        return False
    
    return dp(0)
```

---

## 11. Infra-relevant hashmap problems

These are problems you'd actually encounter in DevOps/SRE work, using the same patterns.

### Problem: IP address request counter (rate limiting)

```python
from collections import defaultdict
import time

class RateLimiter:
    def __init__(self, max_requests, window_seconds):
        self.max_requests = max_requests
        self.window = window_seconds
        self.requests = defaultdict(list)  # ip → [timestamps]
    
    def allow(self, ip, timestamp):
        # Clean old requests
        cutoff = timestamp - self.window
        self.requests[ip] = [t for t in self.requests[ip] if t > cutoff]
        
        if len(self.requests[ip]) < self.max_requests:
            self.requests[ip].append(timestamp)
            return True
        return False

# Usage: limiter.allow("192.168.1.1", time.time())
```

### Problem: Log deduplication

```python
class LogDeduplicator:
    """Suppress duplicate log messages within a time window"""
    
    def __init__(self, window_seconds):
        self.window = window_seconds
        self.last_seen = {}  # message_hash → timestamp
    
    def should_log(self, timestamp, message):
        msg_hash = hash(message)
        
        if msg_hash not in self.last_seen:
            self.last_seen[msg_hash] = timestamp
            return True
        
        if timestamp - self.last_seen[msg_hash] >= self.window:
            self.last_seen[msg_hash] = timestamp
            return True
        
        return False
```

### Problem: Service dependency tracker

```python
def find_all_dependencies(services, target):
    """
    services = {"api": ["auth", "db"], "auth": ["db", "cache"], "db": [], "cache": []}
    find_all_dependencies(services, "api") → {"auth", "db", "cache"}
    """
    visited = set()
    
    def dfs(service):
        for dep in services.get(service, []):
            if dep not in visited:
                visited.add(dep)
                dfs(dep)
    
    dfs(target)
    return visited
```

### Problem: Config diff — find changed, added, removed keys

```python
def config_diff(old_config, new_config):
    old_keys = set(old_config.keys())
    new_keys = set(new_config.keys())
    
    added = new_keys - old_keys
    removed = old_keys - new_keys
    common = old_keys & new_keys
    changed = {k for k in common if old_config[k] != new_config[k]}
    
    return {
        "added": {k: new_config[k] for k in added},
        "removed": {k: old_config[k] for k in removed},
        "changed": {k: {"old": old_config[k], "new": new_config[k]} for k in changed},
    }
```

### Problem: DNS cache with TTL

```python
import time

class DNSCache:
    def __init__(self):
        self.cache = {}  # domain → (ip, expire_time)
    
    def resolve(self, domain, ttl=300):
        if domain in self.cache:
            ip, expires = self.cache[domain]
            if time.time() < expires:
                return ip  # cache hit
            else:
                del self.cache[domain]  # expired
        return None  # cache miss
    
    def store(self, domain, ip, ttl=300):
        self.cache[domain] = (ip, time.time() + ttl)
    
    def evict_expired(self):
        now = time.time()
        expired = [d for d, (_, exp) in self.cache.items() if now >= exp]
        for d in expired:
            del self.cache[d]
```

### Problem: Aggregate metrics by label (Prometheus-style)

```python
def aggregate_metrics(data_points):
    """
    data_points = [
        {"metric": "http_requests", "method": "GET", "status": "200", "value": 42},
        {"metric": "http_requests", "method": "GET", "status": "200", "value": 18},
        {"metric": "http_requests", "method": "POST", "status": "500", "value": 3},
    ]
    
    Group by (metric, labels) and sum values.
    """
    aggregated = defaultdict(float)
    
    for dp in data_points:
        # Create a hashable key from metric name + all labels
        labels = {k: v for k, v in dp.items() if k not in ("metric", "value")}
        key = (dp["metric"], tuple(sorted(labels.items())))
        aggregated[key] += dp["value"]
    
    return dict(aggregated)

# Result:
# {("http_requests", (("method","GET"),("status","200"))): 60,
#  ("http_requests", (("method","POST"),("status","500"))): 3}
```

---

## 12. LeetCode problem list (25 problems)

### Easy (15 min each)

| # | Problem | Pattern | Key takeaway |
|---|---------|---------|-------------|
| 1 | Two Sum | Lookup optimization | Complement in hashmap |
| 217 | Contains Duplicate | Set existence | set() for O(1) check |
| 242 | Valid Anagram | Frequency counting | Counter comparison |
| 383 | Ransom Note | Frequency counting | Counter subtraction |
| 387 | First Unique Character | Two-pass frequency | Count then scan |
| 169 | Majority Element | Frequency / Boyer-Moore | O(1) space variant |
| 349 | Intersection of Two Arrays | Set operations | set intersection |
| 205 | Isomorphic Strings | Bidirectional mapping | Two dicts needed |
| 290 | Word Pattern | Bidirectional mapping | Same as isomorphic |
| 219 | Contains Duplicate II | Index tracking | last_seen dict |

### Medium (30 min each)

| # | Problem | Pattern | Key takeaway |
|---|---------|---------|-------------|
| 49 | Group Anagrams | Grouping | sorted tuple as key |
| 347 | Top K Frequent Elements | Frequency + bucket sort | O(n) with buckets |
| 128 | Longest Consecutive Sequence | Set + smart start | Only count from sequence start |
| 560 | Subarray Sum Equals K | Prefix sum + hashmap | Complement lookup |
| 523 | Continuous Subarray Sum | Prefix sum + remainder | Modulo hashmap |
| 438 | Find All Anagrams | Sliding window + Counter | Fixed window Counter compare |
| 567 | Permutation in String | Sliding window + Counter | Same as anagrams |
| 451 | Sort Characters by Frequency | Frequency + sort | Counter → sorted output |
| 36 | Valid Sudoku | Multi-set tracking | rows, cols, boxes sets |
| 299 | Bulls and Cows | Counter intersection | Exact vs partial match |
| 139 | Word Break | Memoization + set | Set for O(1) word lookup |
| 442 | Find All Duplicates | Index tracking / marking | Array as its own hashmap |

### Hard (attempt after Medium is comfortable)

| # | Problem | Pattern | Key takeaway |
|---|---------|---------|-------------|
| 76 | Minimum Window Substring | Sliding window + Counter | Track "missing" count |
| 380 | Insert Delete GetRandom O(1) | Dict + array swap | Dict for index, array for random |
| 146 | LRU Cache | Dict + doubly linked list | OrderedDict shortcut |

---

## 13. Interview tips for hashmap problems

### Tip 1: State the brute force first

Always say: "The brute force is O(n²) with nested loops. But I can use a hashmap to bring it to O(n)." This shows problem-solving progression.

### Tip 2: Name your hashmaps descriptively

```python
# Bad
d = {}

# Good
complement_index = {}    # complement_value → index
char_frequency = {}      # character → count
last_seen = {}           # element → last index
prefix_count = {}        # prefix_sum → number of occurrences
```

### Tip 3: Use .get() to avoid KeyError

```python
# Fragile — crashes on missing key
count = d[key] + 1

# Safe — defaults to 0 if missing
count = d.get(key, 0) + 1
```

### Tip 4: Know when to use set vs dict

```python
# Just need existence check? → set
seen = set()
if x in seen: ...

# Need to associate data with the key? → dict
index_of = {}
index_of[x] = i
```

### Tip 5: Clean up zero-count entries in window hashmaps

```python
# When shrinking a sliding window, delete keys with count 0
count[char] -= 1
if count[char] == 0:
    del count[char]    # keeps len(count) accurate for "distinct count" checks
```

### Tip 6: Use tuple as hashmap key for composite keys

```python
# Grouping by multiple attributes
key = (row // 3, col // 3)     # Sudoku box ID
key = tuple(sorted(word))      # anagram signature
key = (x, y)                   # coordinate pair
```

---

## 14. Common mistakes

### Mistake 1: Forgetting that dict preserves insertion order (Python 3.7+)

```python
# Python 3.7+ dicts maintain insertion order
# But don't rely on this for algorithmic correctness
# Use OrderedDict if order is part of the algorithm (e.g., LRU cache)
from collections import OrderedDict
```

### Mistake 2: Mutating dict while iterating

```python
# WRONG — RuntimeError: dictionary changed size during iteration
for key in d:
    if some_condition:
        del d[key]

# RIGHT — iterate over a copy of keys
for key in list(d.keys()):
    if some_condition:
        del d[key]

# RIGHT — build a new dict
d = {k: v for k, v in d.items() if not some_condition}
```

### Mistake 3: Using list as dict key

```python
# WRONG — lists are unhashable
d[[1, 2, 3]] = "value"    # TypeError!

# RIGHT — convert to tuple
d[tuple([1, 2, 3])] = "value"    # works
d[(1, 2, 3)] = "value"           # same thing
```

### Mistake 4: Not initializing hashmap correctly

```python
# WRONG — KeyError on first access
count = {}
count["a"] += 1    # KeyError!

# RIGHT options:
count = {}
count["a"] = count.get("a", 0) + 1

count = defaultdict(int)
count["a"] += 1    # starts at 0, no error

count = Counter()
count["a"] += 1    # same as defaultdict(int) for counting
```

### Mistake 5: Comparing Counter objects incorrectly

```python
# Counter with 0 values vs missing keys
c1 = Counter({'a': 1, 'b': 0})
c2 = Counter({'a': 1})

c1 == c2    # True! Counter ignores zero-count entries in comparison

# But:
len(c1)     # 2 (includes 'b' with count 0)
len(c2)     # 1

# If you need exact key matching, compare dicts instead
dict(c1) == dict(c2)    # False
```

### Mistake 6: Space complexity — hashmaps use O(n) space

```python
# If interviewer asks for O(1) space, hashmap is NOT the answer
# Common O(1) space alternatives:
# - Two-pointer
# - Boyer-Moore voting
# - Using input array as storage (marking by negation)
# - Math/bit manipulation
```

---

## 15. Cheat sheet

### Pattern recognition

```
"Find pair/complement"               → Hashmap lookup (Two Sum pattern)
"Count / frequency / most common"    → Counter or manual dict counting
"Group by some property"             → defaultdict(list) with computed key
"Check anagram / permutation"        → Counter comparison
"Find duplicates"                    → Set or Counter
"Subarray sum equals K"              → Prefix sum stored in hashmap
"Sliding window + unique tracking"   → Hashmap tracks window state
"Cache computed results"             → Memoization dict / @lru_cache
"Track last occurrence"              → Dict mapping element → index
"Need O(1) for insert/lookup/delete" → Hashmap is the answer
```

### Time complexity

```
dict/set lookup (x in d):          O(1)
dict/set insert (d[x] = v):       O(1)
dict/set delete (del d[x]):       O(1)
dict iteration:                    O(n)
Counter(list):                     O(n)
Counter.most_common(k):            O(n log n) or O(n log k) with heap
set intersection (a & b):          O(min(len(a), len(b)))
set union (a | b):                 O(len(a) + len(b))
```

### Python shortcuts

```python
# Counting
Counter(arr)                        # frequency map
Counter(arr).most_common(k)         # top k elements

# Grouping
d = defaultdict(list)
d[key].append(value)                # auto-creates list

# Set operations
set(a) & set(b)                     # common elements
set(a) - set(b)                     # elements in a but not b
set(a) | set(b)                     # all elements from both
set(a) ^ set(b)                     # elements in exactly one

# Safe access
d.get(key, default)                 # no KeyError
d.setdefault(key, []).append(val)   # create if missing, then append
d.pop(key, None)                    # remove, no error if missing
```

### When NOT to use a hashmap

```
Array is sorted                     → Two-pointer (O(1) space)
Need sorted order of keys           → Use sorted() or SortedDict
Need min/max efficiently            → Heap
Space must be O(1)                  → Two-pointer, Boyer-Moore, bit ops
Keys are small integers (0-n)       → Use array instead of hashmap
Need ordered operations             → BST or SortedList
```

---

## Study plan for this section

| Day | Focus | Problems | Target |
|-----|-------|----------|--------|
| 1 | Lookup optimization | LC 1, 217, 349, 128 | Hashmap replaces inner loop |
| 2 | Frequency counting | LC 242, 387, 347, 169 | Counter fluency |
| 3 | Grouping | LC 49, 205, 290, 36 | Computed keys, bidirectional maps |
| 4 | Hashmap + sliding window | LC 567, 438, 340 | Window state in hashmap |
| 5 | Hashmap + prefix sum | LC 560, 523 | Prefix complement lookup |
| 6 | Mixed practice (timed) | LC 139, 451, 299 | Pattern recognition speed |
| 7 | Infra problems | Rate limiter, DNS cache, config diff | Real-world application |

**Daily minimum:** 3 problems. State time and space complexity for each. Explain out loud.

---

*Next topic: Graphs — BFS, DFS, topological sort (dependency resolution), shortest path*
