# Arrays & Strings — Complete MAANG Interview Guide
## Two-pointer, Sliding window, Prefix sums

> **Target:** Solve 70% of LC Medium array/string problems in 30 minutes
> **Why this matters:** Arrays are the foundation of 60%+ of all coding interview questions. Every pattern here appears in infra-focused interviews too — log parsing, IP range analysis, metrics windows, resource allocation.

---

## Table of contents

1. [Big-O refresher](#1-big-o-refresher)
2. [Arrays fundamentals](#2-arrays-fundamentals)
3. [Strings fundamentals](#3-strings-fundamentals)
4. [Pattern 1: Two-pointer](#4-pattern-1-two-pointer)
5. [Pattern 2: Sliding window](#5-pattern-2-sliding-window)
6. [Pattern 3: Prefix sums](#6-pattern-3-prefix-sums)
7. [Pattern 4: Frequency counting](#7-pattern-4-frequency-counting)
8. [Pattern 5: In-place array manipulation](#8-pattern-5-in-place-array-manipulation)
9. [Combined patterns](#9-combined-patterns)
10. [Infra-relevant coding problems](#10-infra-relevant-coding-problems)
11. [LeetCode problem list (30 problems)](#11-leetcode-problem-list-30-problems)
12. [Interview framework](#12-interview-framework)
13. [Common mistakes](#13-common-mistakes)
14. [Cheat sheet](#14-cheat-sheet)

---

## 1. Big-O refresher

Before any code, you need to think about complexity instinctively. Interviewers expect you to state it without being asked.

| Complexity | Name | Example | 1M items |
|---|---|---|---|
| O(1) | Constant | Dict lookup, array index access | 1 operation |
| O(log n) | Logarithmic | Binary search | ~20 operations |
| O(n) | Linear | Single loop through array | 1M operations |
| O(n log n) | Linearithmic | Sorting (Python's sorted()) | ~20M operations |
| O(n²) | Quadratic | Nested loops | 1 TRILLION operations |
| O(2^n) | Exponential | All subsets | Universe heat death |

**Practical rule for MAANG:** Inputs are 10K–100K items. O(n) or O(n log n) pass. O(n²) is usually too slow. If you write a nested loop, ask "can I replace the inner loop with a hashmap/two-pointer/binary search?"

### Space complexity

- O(1) — fixed extra memory (few variables)
- O(n) — extra memory proportional to input (hashmap, copy of array)
- In-place algorithms use O(1) extra space — interviewers love these

---

## 2. Arrays fundamentals

### Python array operations and their complexity

```python
# O(1) operations
arr[i]              # access by index
arr[i] = val        # set by index
arr.append(val)     # add to end (amortized O(1))
len(arr)            # length

# O(n) operations
arr.insert(i, val)  # insert at index — shifts everything after
arr.remove(val)     # remove first occurrence — shifts everything after
arr.pop(0)          # remove from front — shifts everything (use deque instead)
val in arr          # search in list — linear scan
arr.copy()          # shallow copy
arr[::-1]           # reverse

# O(n log n)
arr.sort()          # in-place sort (Timsort)
sorted(arr)         # returns new sorted array

# O(k) where k is slice size
arr[i:j]            # slicing creates a new list
```

### Key gotcha: list vs deque

```python
from collections import deque

# If you need to add/remove from BOTH ends:
# list.pop(0) is O(n) — shifts everything
# deque.popleft() is O(1)

q = deque()
q.append(1)       # add right — O(1)
q.appendleft(2)   # add left — O(1)
q.pop()            # remove right — O(1)
q.popleft()        # remove left — O(1)
```

### Sorting — know these details

```python
# Default sort (ascending)
arr.sort()                      # in-place, returns None
new_arr = sorted(arr)           # returns new list

# Custom sort
arr.sort(key=lambda x: x[1])   # sort by second element of tuples
arr.sort(key=lambda x: -x)     # descending (negate for numbers)
arr.sort(reverse=True)          # descending

# Sort is STABLE — equal elements keep their original order
# This matters when sorting by multiple criteria:
# Sort by priority, then by name:
tasks.sort(key=lambda x: x.name)    # secondary sort first
tasks.sort(key=lambda x: x.priority) # primary sort second

# Or use tuple key (sorts lexicographically):
tasks.sort(key=lambda x: (x.priority, x.name))
```

---

## 3. Strings fundamentals

### Python strings — immutable

Strings cannot be modified in place. Every operation creates a new string.

```python
# O(n) operations
s.find(sub)         # find substring, returns index or -1
s.count(sub)        # count occurrences
s.split(sep)        # split into list
s.strip()           # remove whitespace
s.replace(old, new) # replace all occurrences
s[::-1]             # reverse
s.lower() / s.upper()

# O(1) operations
s[i]                # access character
len(s)              # length
ord(c)              # character to ASCII code
chr(n)              # ASCII code to character
```

### Critical: String concatenation in a loop is O(n²)

```python
# BAD — O(n²) because each += creates a new string
result = ""
for char in data:
    result += char      # copies entire string each time

# GOOD — O(n) using list + join
parts = []
for char in data:
    parts.append(char)  # O(1) amortized
result = "".join(parts) # one copy at the end

# GOOD — list comprehension
result = "".join(char for char in data if char.isalpha())
```

### Converting between strings and arrays

```python
# String → list of characters
chars = list("hello")          # ['h', 'e', 'l', 'l', 'o']

# List → string
s = "".join(chars)             # "hello"

# String → list of words
words = "hello world".split()  # ['hello', 'world']

# List of words → string
s = " ".join(words)            # "hello world"
```

---

## 4. Pattern 1: Two-pointer

### When to use

- Array is **sorted** (or you can sort it)
- Looking for **pairs** that satisfy a condition
- Comparing elements from **both ends**
- **Removing duplicates** in-place
- **Partitioning** an array

### How it works

Place one pointer at the start, one at the end (or both at the start). Move them toward each other based on a condition. This eliminates the need for a nested loop — O(n) instead of O(n²).

### Variant 1: Opposite direction (start + end)

Used when the array is sorted and you're looking for pairs.

#### Problem: Two Sum II (sorted array)
Given a sorted array, find two numbers that add up to target. Return indices.

```python
def two_sum_sorted(numbers, target):
    left, right = 0, len(numbers) - 1
    
    while left < right:
        current_sum = numbers[left] + numbers[right]
        
        if current_sum == target:
            return [left, right]
        elif current_sum < target:
            left += 1       # need bigger sum, move left forward
        else:
            right -= 1      # need smaller sum, move right backward
    
    return []  # no pair found

# Example: numbers = [2, 7, 11, 15], target = 9
# left=0 (2), right=3 (15): sum=17 > 9, move right
# left=0 (2), right=2 (11): sum=13 > 9, move right
# left=0 (2), right=1 (7): sum=9 == 9, return [0, 1]
```

**Why this works:** In a sorted array, if the sum is too big, moving the right pointer left makes it smaller. If too small, moving left pointer right makes it bigger. Every step eliminates one possibility, so we check all pairs in O(n).

**Time: O(n), Space: O(1)**

#### Problem: Container With Most Water (LC #11, Medium)
Given heights, find two lines that form a container holding the most water.

```python
def max_area(height):
    left, right = 0, len(height) - 1
    max_water = 0
    
    while left < right:
        width = right - left
        h = min(height[left], height[right])
        max_water = max(max_water, width * h)
        
        # Move the shorter side inward (it's the bottleneck)
        if height[left] < height[right]:
            left += 1
        else:
            right -= 1
    
    return max_water

# Why move the shorter side?
# Water is limited by the shorter line.
# Moving the taller line can only make width smaller and height stays same or gets worse.
# Moving the shorter line might find a taller line, increasing height.
```

**Time: O(n), Space: O(1)**

#### Problem: 3Sum (LC #15, Medium) — extremely common
Find all unique triplets that sum to zero.

```python
def three_sum(nums):
    nums.sort()  # sort first — enables two-pointer
    result = []
    
    for i in range(len(nums) - 2):
        # Skip duplicates for first element
        if i > 0 and nums[i] == nums[i - 1]:
            continue
        
        # Two-pointer for remaining pair
        left, right = i + 1, len(nums) - 1
        
        while left < right:
            total = nums[i] + nums[left] + nums[right]
            
            if total == 0:
                result.append([nums[i], nums[left], nums[right]])
                # Skip duplicates
                while left < right and nums[left] == nums[left + 1]:
                    left += 1
                while left < right and nums[right] == nums[right - 1]:
                    right -= 1
                left += 1
                right -= 1
            elif total < 0:
                left += 1
            else:
                right -= 1
    
    return result

# Example: nums = [-1, 0, 1, 2, -1, -4]
# Sorted: [-4, -1, -1, 0, 1, 2]
# i=0 (-4): two-pointer finds nothing summing to 4
# i=1 (-1): two-pointer finds [-1, 0, 1] and [-1, -1, 2]
# i=2 (-1): skip (duplicate of i=1)
# Result: [[-1, -1, 2], [-1, 0, 1]]
```

**Time: O(n²) — sorting is O(n log n) + nested loop is O(n²). Space: O(1) extra (ignoring output)**

### Variant 2: Same direction (slow + fast pointer)

Used for removing elements, deduplication, or detecting cycles.

#### Problem: Remove Duplicates from Sorted Array (LC #26, Easy)
Remove duplicates in-place, return new length.

```python
def remove_duplicates(nums):
    if not nums:
        return 0
    
    slow = 0  # points to last unique element
    
    for fast in range(1, len(nums)):
        if nums[fast] != nums[slow]:
            slow += 1
            nums[slow] = nums[fast]
    
    return slow + 1

# Example: [1, 1, 2, 3, 3]
# slow=0(1), fast=1(1): equal, skip
# slow=0(1), fast=2(2): different, slow→1, nums[1]=2 → [1, 2, 2, 3, 3]
# slow=1(2), fast=3(3): different, slow→2, nums[2]=3 → [1, 2, 3, 3, 3]
# slow=2(3), fast=4(3): equal, skip
# Return 3, array is [1, 2, 3, ...]
```

**Time: O(n), Space: O(1)**

#### Problem: Move Zeroes (LC #283, Easy)
Move all zeroes to end while maintaining order of non-zero elements.

```python
def move_zeroes(nums):
    slow = 0  # position where next non-zero should go
    
    for fast in range(len(nums)):
        if nums[fast] != 0:
            nums[slow], nums[fast] = nums[fast], nums[slow]
            slow += 1

# Example: [0, 1, 0, 3, 12]
# fast=0(0): zero, skip
# fast=1(1): swap nums[0],nums[1] → [1, 0, 0, 3, 12], slow=1
# fast=2(0): zero, skip
# fast=3(3): swap nums[1],nums[3] → [1, 3, 0, 0, 12], slow=2
# fast=4(12): swap nums[2],nums[4] → [1, 3, 12, 0, 0], slow=3
```

**Time: O(n), Space: O(1)**

### Variant 3: Palindrome check

```python
def is_palindrome(s):
    # Clean string: only alphanumeric, lowercase
    s = ''.join(c.lower() for c in s if c.isalnum())
    
    left, right = 0, len(s) - 1
    while left < right:
        if s[left] != s[right]:
            return False
        left += 1
        right -= 1
    
    return True
```

### Two-pointer decision guide

```
Is the array sorted (or can you sort it)?
├── YES: looking for pairs/triplets summing to target?
│   └── Opposite direction pointers (start + end)
├── YES: need to remove/deduplicate in-place?
│   └── Same direction pointers (slow + fast)
├── NO: need to compare from both ends (palindrome, container)?
│   └── Opposite direction pointers
└── NO: consider sorting first, or use hashmap instead
```

---

## 5. Pattern 2: Sliding window

### When to use

- Find **subarray/substring** of certain size or condition
- "Longest/shortest substring with..."
- "Maximum sum of subarray of size K"
- Moving average, rate limiting, log time windows
- Any time you see **contiguous** sequence + **optimization**

### How it works

Maintain a "window" defined by two pointers (left and right). Expand the window by moving right. When the window violates a condition, shrink by moving left. This avoids recalculating from scratch for every position — O(n) instead of O(n²).

### Variant 1: Fixed-size window

Window size is given. Slide it across the array.

#### Problem: Maximum Sum Subarray of Size K

```python
def max_sum_subarray(nums, k):
    # Build first window
    window_sum = sum(nums[:k])
    max_sum = window_sum
    
    # Slide the window: add right element, remove left element
    for i in range(k, len(nums)):
        window_sum += nums[i]       # add new right
        window_sum -= nums[i - k]   # remove old left
        max_sum = max(max_sum, window_sum)
    
    return max_sum

# Example: nums = [2, 1, 5, 1, 3, 2], k = 3
# Window [2,1,5] sum=8
# Slide: add 1, remove 2 → [1,5,1] sum=7
# Slide: add 3, remove 1 → [5,1,3] sum=9 ← max
# Slide: add 2, remove 5 → [1,3,2] sum=6
# Answer: 9
```

**Time: O(n), Space: O(1)**

**Infra application:** Calculate moving average of request latency over a 5-minute window. Same pattern — fixed-size window sliding over time-series data.

#### Problem: Moving Average of Data Stream

```python
from collections import deque

class MovingAverage:
    def __init__(self, size):
        self.size = size
        self.window = deque()
        self.window_sum = 0
    
    def next(self, val):
        self.window.append(val)
        self.window_sum += val
        
        if len(self.window) > self.size:
            self.window_sum -= self.window.popleft()
        
        return self.window_sum / len(self.window)

# This is literally how monitoring systems calculate moving averages
```

### Variant 2: Variable-size window (most common in interviews)

Window size is not given. You expand until a condition breaks, then shrink until it's valid again.

#### Template — memorize this

```python
def sliding_window_template(s_or_arr):
    left = 0
    # state tracking (hashmap, counter, sum, etc.)
    result = 0  # or float('inf') for minimum problems
    
    for right in range(len(s_or_arr)):
        # 1. EXPAND: add s_or_arr[right] to window state
        
        # 2. SHRINK: while window is invalid, remove s_or_arr[left]
        while window_is_invalid():
            # remove s_or_arr[left] from window state
            left += 1
        
        # 3. UPDATE: record the result (window is now valid)
        result = max(result, right - left + 1)  # for longest
        # result = min(result, right - left + 1)  # for shortest
    
    return result
```

#### Problem: Longest Substring Without Repeating Characters (LC #3, Medium)
Find the length of the longest substring with all unique characters.

```python
def length_of_longest_substring(s):
    char_index = {}  # char → last seen index
    left = 0
    max_length = 0
    
    for right in range(len(s)):
        char = s[right]
        
        # If char was seen and is inside current window, shrink
        if char in char_index and char_index[char] >= left:
            left = char_index[char] + 1
        
        char_index[char] = right
        max_length = max(max_length, right - left + 1)
    
    return max_length

# Example: s = "abcabcbb"
# right=0 'a': window="a", len=1, max=1
# right=1 'b': window="ab", len=2, max=2
# right=2 'c': window="abc", len=3, max=3
# right=3 'a': 'a' seen at 0, left→1, window="bca", len=3, max=3
# right=4 'b': 'b' seen at 1, left→2, window="cab", len=3, max=3
# right=5 'c': 'c' seen at 2, left→3, window="abc", len=3, max=3
# right=6 'b': 'b' seen at 4, left→5, window="cb", len=2, max=3
# right=7 'b': 'b' seen at 6, left→7, window="b", len=1, max=3
# Answer: 3
```

**Time: O(n), Space: O(min(n, alphabet_size))**

#### Problem: Minimum Window Substring (LC #76, Hard — but very common)
Find the smallest window in s that contains all characters of t.

```python
from collections import Counter

def min_window(s, t):
    if not t or not s:
        return ""
    
    # Count characters needed
    need = Counter(t)
    missing = len(t)  # total characters still needed
    
    left = 0
    min_start = 0
    min_len = float('inf')
    
    for right in range(len(s)):
        # EXPAND: add s[right]
        if s[right] in need:
            if need[s[right]] > 0:
                missing -= 1
            need[s[right]] -= 1
        
        # SHRINK: while window contains all of t
        while missing == 0:
            # Update result
            window_len = right - left + 1
            if window_len < min_len:
                min_len = window_len
                min_start = left
            
            # Remove s[left] from window
            if s[left] in need:
                need[s[left]] += 1
                if need[s[left]] > 0:
                    missing += 1
            left += 1
    
    return "" if min_len == float('inf') else s[min_start:min_start + min_len]

# Example: s = "ADOBECODEBANC", t = "ABC"
# Answer: "BANC" (positions 9-12)
```

**Time: O(n), Space: O(k) where k is unique chars in t**

#### Problem: Longest Substring with At Most K Distinct Characters (LC #340, Medium)

```python
def longest_k_distinct(s, k):
    char_count = {}
    left = 0
    max_length = 0
    
    for right in range(len(s)):
        # EXPAND
        char_count[s[right]] = char_count.get(s[right], 0) + 1
        
        # SHRINK: too many distinct characters
        while len(char_count) > k:
            char_count[s[left]] -= 1
            if char_count[s[left]] == 0:
                del char_count[s[left]]
            left += 1
        
        # UPDATE
        max_length = max(max_length, right - left + 1)
    
    return max_length
```

#### Problem: Maximum Number of Occurrences of a Substring (infra-relevant)
Count occurrences of substrings in a log pattern — variable window with hashmap.

```python
def max_freq_substring(s, max_letters, min_size, max_size):
    # Key insight: only check min_size windows
    # If a string of length min_size appears often,
    # any longer string containing it appears AT MOST as often
    count = {}
    
    for i in range(len(s) - min_size + 1):
        sub = s[i:i + min_size]
        unique = len(set(sub))
        if unique <= max_letters:
            count[sub] = count.get(sub, 0) + 1
    
    return max(count.values()) if count else 0
```

### Sliding window decision guide

```
Is the window size fixed?
├── YES: Use fixed-size template (add right, remove left, track state)
└── NO: Variable-size window
    ├── Looking for LONGEST valid window?
    │   └── Expand right always, shrink left only when invalid
    ├── Looking for SHORTEST valid window?
    │   └── Expand right until valid, then shrink left while still valid
    └── How to track window state?
        ├── Unique characters → hashmap of char→count
        ├── Sum constraint → running sum
        └── Frequency constraint → Counter + "missing" count
```

---

## 6. Pattern 3: Prefix sums

### When to use

- "Sum of subarray from index i to j" — multiple queries
- "Number of subarrays with sum equal to K"
- "Is there a subarray with sum zero?"
- Range queries on cumulative data
- Any time you see **subarray sum** in the problem

### How it works

Build an array where `prefix[i]` = sum of all elements from index 0 to i-1. Then the sum of any subarray `nums[i..j]` = `prefix[j+1] - prefix[i]`. One-time O(n) build, then O(1) per query.

### Basic prefix sum

```python
def build_prefix_sum(nums):
    prefix = [0] * (len(nums) + 1)
    for i in range(len(nums)):
        prefix[i + 1] = prefix[i] + nums[i]
    return prefix

# nums:   [2, 4, 1, 3, 5]
# prefix: [0, 2, 6, 7, 10, 15]
#
# Sum of nums[1..3] (4 + 1 + 3 = 8):
# prefix[4] - prefix[1] = 10 - 2 = 8  ✓
#
# Sum of nums[0..4] (entire array):
# prefix[5] - prefix[0] = 15 - 0 = 15  ✓

def range_sum(prefix, i, j):
    """Sum of nums[i..j] inclusive"""
    return prefix[j + 1] - prefix[i]
```

### Problem: Subarray Sum Equals K (LC #560, Medium) — very common

Find the number of contiguous subarrays that sum to K.

```python
def subarray_sum(nums, k):
    count = 0
    current_sum = 0
    prefix_counts = {0: 1}  # prefix_sum → how many times we've seen it
    
    for num in nums:
        current_sum += num
        
        # If (current_sum - k) was a previous prefix sum,
        # then the subarray between that point and here sums to k
        if current_sum - k in prefix_counts:
            count += prefix_counts[current_sum - k]
        
        prefix_counts[current_sum] = prefix_counts.get(current_sum, 0) + 1
    
    return count

# Example: nums = [1, 2, 3], k = 3
# num=1: sum=1, need 1-3=-2 (not found), store {0:1, 1:1}
# num=2: sum=3, need 3-3=0 (found! count=1), store {0:1, 1:1, 3:1}
# num=3: sum=6, need 6-3=3 (found! count=2), store {0:1, 1:1, 3:1, 6:1}
# Answer: 2 (subarrays [1,2] and [3])
```

**Time: O(n), Space: O(n)**

**Why this works:** If `prefix[j] - prefix[i] = k`, then the subarray from i to j sums to k. We track all previous prefix sums in a hashmap. At each position, we check if `current_sum - k` exists as a previous prefix sum.

### Problem: Contiguous Array (LC #525, Medium)
Find the maximum length subarray with equal number of 0s and 1s.

```python
def find_max_length(nums):
    # Trick: treat 0 as -1, then find longest subarray with sum 0
    count = 0  # running sum (0 becomes -1)
    max_length = 0
    first_seen = {0: -1}  # sum → first index where this sum occurred
    
    for i in range(len(nums)):
        count += 1 if nums[i] == 1 else -1
        
        if count in first_seen:
            max_length = max(max_length, i - first_seen[count])
        else:
            first_seen[count] = i
    
    return max_length

# Example: nums = [0, 1, 0, 1, 1, 0]
# Transform to:   [-1, 1, -1, 1, 1, -1]
# Running sum:     -1, 0, -1, 0, 1, 0
# sum=0 first at -1, last at 5: length = 5-(-1) = 6 → entire array
```

### Problem: Product of Array Except Self (LC #238, Medium)
Build prefix products from left and right.

```python
def product_except_self(nums):
    n = len(nums)
    result = [1] * n
    
    # Left prefix products
    left_product = 1
    for i in range(n):
        result[i] = left_product
        left_product *= nums[i]
    
    # Right prefix products (multiply into result)
    right_product = 1
    for i in range(n - 1, -1, -1):
        result[i] *= right_product
        right_product *= nums[i]
    
    return result

# Example: nums = [1, 2, 3, 4]
# Left pass:  result = [1, 1, 2, 6]
# Right pass: result = [24, 12, 8, 6]
# Verify: [2*3*4, 1*3*4, 1*2*4, 1*2*3] = [24, 12, 8, 6] ✓
```

**Time: O(n), Space: O(1) extra (result doesn't count)**

### Infra application: Rate limiting with prefix sums

```python
class RateLimiter:
    """Count requests in a sliding time window using prefix sum concept"""
    
    def __init__(self, max_requests, window_seconds):
        self.max_requests = max_requests
        self.window = window_seconds
        self.requests = []  # sorted timestamps
    
    def allow_request(self, timestamp):
        # Remove expired requests
        cutoff = timestamp - self.window
        while self.requests and self.requests[0] <= cutoff:
            self.requests.pop(0)
        
        if len(self.requests) < self.max_requests:
            self.requests.append(timestamp)
            return True
        return False
```

---

## 7. Pattern 4: Frequency counting

### When to use

- "Most common" / "least common" element
- Anagram checking
- "Contains duplicate"
- Grouping by some attribute

### Counter basics

```python
from collections import Counter

# Count frequencies
freq = Counter([1, 2, 2, 3, 3, 3])
# Counter({3: 3, 2: 2, 1: 1})

freq.most_common(2)    # [(3, 3), (2, 2)]
freq[4]                # 0 (missing keys return 0)

# Manual counting (when you can't import Counter)
freq = {}
for item in arr:
    freq[item] = freq.get(item, 0) + 1
```

### Problem: Group Anagrams (LC #49, Medium)

```python
from collections import defaultdict

def group_anagrams(strs):
    groups = defaultdict(list)
    
    for s in strs:
        # Sorted string is the "signature" for anagrams
        key = tuple(sorted(s))
        groups[key].append(s)
    
    return list(groups.values())

# Example: ["eat", "tea", "tan", "ate", "nat", "bat"]
# Signatures:
#   ('a','e','t') → ["eat", "tea", "ate"]
#   ('a','n','t') → ["tan", "nat"]
#   ('a','b','t') → ["bat"]
```

**Time: O(n * k log k) where k is max string length**

### Problem: Top K Frequent Elements (LC #347, Medium)

```python
def top_k_frequent(nums, k):
    freq = Counter(nums)
    return [item for item, count in freq.most_common(k)]

# O(n log n) with most_common, but can be O(n) with bucket sort:
def top_k_frequent_optimal(nums, k):
    freq = Counter(nums)
    
    # Bucket sort: index = frequency, value = list of elements
    buckets = [[] for _ in range(len(nums) + 1)]
    for num, count in freq.items():
        buckets[count].append(num)
    
    result = []
    for i in range(len(buckets) - 1, -1, -1):
        for num in buckets[i]:
            result.append(num)
            if len(result) == k:
                return result
    
    return result
```

---

## 8. Pattern 5: In-place array manipulation

### When to use

- "Do it in O(1) extra space"
- Array serves as its own hashmap (values are indices)
- Rearranging elements without extra array

### Problem: First Missing Positive (LC #41, Hard)
Find the smallest missing positive integer. Must be O(n) time, O(1) space.

```python
def first_missing_positive(nums):
    n = len(nums)
    
    # Place each number in its "correct" position
    # Number 1 should be at index 0, number 2 at index 1, etc.
    for i in range(n):
        while 1 <= nums[i] <= n and nums[nums[i] - 1] != nums[i]:
            # Swap nums[i] to its correct position
            correct_idx = nums[i] - 1
            nums[i], nums[correct_idx] = nums[correct_idx], nums[i]
    
    # Find first index where nums[i] != i + 1
    for i in range(n):
        if nums[i] != i + 1:
            return i + 1
    
    return n + 1

# Example: [3, 4, -1, 1]
# After swapping: [1, -1, 3, 4]
# Index 1 has -1 instead of 2 → answer is 2
```

### Problem: Rotate Array (LC #189, Medium)

```python
def rotate(nums, k):
    n = len(nums)
    k = k % n  # handle k > n
    
    # Reverse entire array, then reverse first k, then reverse rest
    def reverse(left, right):
        while left < right:
            nums[left], nums[right] = nums[right], nums[left]
            left += 1
            right -= 1
    
    reverse(0, n - 1)      # [1,2,3,4,5] → [5,4,3,2,1]
    reverse(0, k - 1)      # [5,4,3,2,1] → [4,5,3,2,1] (k=2)
    reverse(k, n - 1)      # [4,5,3,2,1] → [4,5,1,2,3]
```

**Time: O(n), Space: O(1)**

---

## 9. Combined patterns

Real interview problems often combine multiple patterns.

### Problem: Longest Repeating Character Replacement (LC #424, Medium)
Sliding window + frequency counting.

```python
def character_replacement(s, k):
    count = {}
    left = 0
    max_freq = 0  # frequency of most common char in window
    max_length = 0
    
    for right in range(len(s)):
        count[s[right]] = count.get(s[right], 0) + 1
        max_freq = max(max_freq, count[s[right]])
        
        # Window size - max_freq = characters that need replacing
        # If > k, shrink window
        window_size = right - left + 1
        if window_size - max_freq > k:
            count[s[left]] -= 1
            left += 1
        
        max_length = max(max_length, right - left + 1)
    
    return max_length
```

### Problem: Trapping Rain Water (LC #42, Hard)
Two-pointer + running max.

```python
def trap(height):
    if not height:
        return 0
    
    left, right = 0, len(height) - 1
    left_max, right_max = height[left], height[right]
    water = 0
    
    while left < right:
        if left_max < right_max:
            left += 1
            left_max = max(left_max, height[left])
            water += left_max - height[left]
        else:
            right -= 1
            right_max = max(right_max, height[right])
            water += right_max - height[right]
    
    return water
```

**Time: O(n), Space: O(1)**

---

## 10. Infra-relevant coding problems

These are the type of coding questions you get in DevOps/SRE interviews — they use the same patterns but feel like real work.

### Problem: Parse CIDR ranges and check IP overlap

```python
def ip_to_int(ip):
    parts = ip.split('.')
    return sum(int(p) << (8 * (3 - i)) for i, p in enumerate(parts))

def cidr_to_range(cidr):
    ip, prefix = cidr.split('/')
    prefix = int(prefix)
    ip_int = ip_to_int(ip)
    mask = (0xFFFFFFFF << (32 - prefix)) & 0xFFFFFFFF
    start = ip_int & mask
    end = start | (~mask & 0xFFFFFFFF)
    return start, end

def cidrs_overlap(cidr1, cidr2):
    s1, e1 = cidr_to_range(cidr1)
    s2, e2 = cidr_to_range(cidr2)
    return s1 <= e2 and s2 <= e1

# Example:
# cidrs_overlap("10.0.0.0/24", "10.0.0.128/25")  → True (subset)
# cidrs_overlap("10.0.0.0/24", "10.0.1.0/24")    → False (adjacent)
```

### Problem: Merge overlapping time intervals (deployment windows)

```python
def merge_intervals(intervals):
    if not intervals:
        return []
    
    intervals.sort(key=lambda x: x[0])
    merged = [intervals[0]]
    
    for start, end in intervals[1:]:
        if start <= merged[-1][1]:
            merged[-1][1] = max(merged[-1][1], end)
        else:
            merged.append([start, end])
    
    return merged

# Example: deployment windows
# [[1, 3], [2, 6], [8, 10], [15, 18]]
# Merged: [[1, 6], [8, 10], [15, 18]]
```

### Problem: Find peak traffic in time-series data (sliding window)

```python
def peak_traffic_window(requests, window_size):
    """Find the time window with maximum request count"""
    if len(requests) < window_size:
        return 0, sum(requests)
    
    window_sum = sum(requests[:window_size])
    max_sum = window_sum
    max_start = 0
    
    for i in range(window_size, len(requests)):
        window_sum += requests[i] - requests[i - window_size]
        if window_sum > max_sum:
            max_sum = window_sum
            max_start = i - window_size + 1
    
    return max_start, max_sum
```

### Problem: Log line deduplication within time window

```python
def dedupe_logs(logs, window_seconds):
    """Remove duplicate log messages within a time window.
    logs = [(timestamp, message), ...]
    """
    seen = {}  # message → last seen timestamp
    result = []
    
    for timestamp, message in logs:
        if message not in seen or timestamp - seen[message] > window_seconds:
            result.append((timestamp, message))
            seen[message] = timestamp
    
    return result
```

---

## 11. LeetCode problem list (30 problems)

### Easy (do these first, aim for 15 min each)

| # | Problem | Pattern | Key concept |
|---|---------|---------|-------------|
| 1 | Two Sum | Hashmap | Complement lookup |
| 26 | Remove Duplicates from Sorted Array | Two-pointer (same dir) | Slow/fast pointer |
| 121 | Best Time to Buy and Sell Stock | Running min | Single pass tracking |
| 125 | Valid Palindrome | Two-pointer (opposite) | Clean + compare |
| 217 | Contains Duplicate | Hashmap/set | Existence check |
| 242 | Valid Anagram | Frequency count | Counter comparison |
| 283 | Move Zeroes | Two-pointer (same dir) | Partition |
| 303 | Range Sum Query - Immutable | Prefix sum | Build once, query O(1) |
| 448 | Find All Numbers Disappeared | In-place marking | Array as hashmap |
| 643 | Maximum Average Subarray I | Fixed sliding window | Slide and track |

### Medium (aim for 30 min each)

| # | Problem | Pattern | Key concept |
|---|---------|---------|-------------|
| 3 | Longest Substring Without Repeating | Sliding window | Variable window + hashmap |
| 11 | Container With Most Water | Two-pointer (opposite) | Move shorter side |
| 15 | 3Sum | Sort + two-pointer | Skip duplicates |
| 49 | Group Anagrams | Frequency/hashmap | Sorted key grouping |
| 53 | Maximum Subarray | Kadane's algorithm | Reset negative running sum |
| 56 | Merge Intervals | Sort + merge | Overlapping ranges |
| 238 | Product of Array Except Self | Prefix/suffix products | Left pass + right pass |
| 347 | Top K Frequent Elements | Frequency + bucket sort | Counting + selection |
| 424 | Longest Repeating Character Replacement | Sliding window + frequency | Window - maxFreq <= k |
| 560 | Subarray Sum Equals K | Prefix sum + hashmap | Complement in prefix map |
| 525 | Contiguous Array | Prefix sum (transform) | Treat 0 as -1 |
| 567 | Permutation in String | Sliding window + Counter | Fixed window anagram |
| 76 | Minimum Window Substring | Sliding window (shrink) | Expand then shrink |
| 340 | Longest Substring with K Distinct | Sliding window | Track distinct count |
| 189 | Rotate Array | Reverse trick | Three reverses |

### Hard (attempt after Medium is comfortable)

| # | Problem | Pattern | Key concept |
|---|---------|---------|-------------|
| 41 | First Missing Positive | In-place swap | Cyclic sort |
| 42 | Trapping Rain Water | Two-pointer | Left max / right max |
| 239 | Sliding Window Maximum | Monotonic deque | Deque tracks max candidates |
| 295 | Find Median from Data Stream | Two heaps | Max-heap + min-heap |
| 4 | Median of Two Sorted Arrays | Binary search | Partition both arrays |

---

## 12. Interview framework

Use this for EVERY problem. Interviewers grade process as much as solution.

### Step 1: Clarify (30 seconds)
```
"Let me make sure I understand the problem..."
- What are the input constraints? (size, value range)
- Can the array be empty?
- Are there negative numbers?
- Is the input sorted?
- Should I return indices or values?
- Can I modify the input array?
```

### Step 2: Examples (1 minute)
```
"Let me trace through an example..."
- Walk through 1-2 small examples by hand
- Include an edge case (empty array, single element)
```

### Step 3: Brute force (30 seconds)
```
"The brute force approach would be... which is O(n²).
 Let me see if I can do better."
- Always acknowledge the naive solution
- This shows you understand the problem before optimizing
```

### Step 4: Optimize (2 minutes)
```
Ask yourself:
- Can a hashmap eliminate the inner loop? (Two Sum pattern)
- Is the array sorted? Can I sort it? (Two-pointer)
- Am I looking at subarrays/substrings? (Sliding window)
- Do I need range sums? (Prefix sum)
- Can I use the array itself as storage? (In-place)
```

### Step 5: Code (10-15 minutes)
```
- Use descriptive variable names (left, right, max_profit — not i, j, m)
- Write helper functions if logic is complex
- Handle edge cases first (empty input, single element)
```

### Step 6: Test (2 minutes)
```
"Let me trace through my code with the example..."
- Walk through with the example input
- Check edge cases: empty, single element, all same, negative
- Check off-by-one errors in indices
```

### Step 7: Complexity (30 seconds)
```
"This runs in O(n) time because we iterate once,
 and O(n) space for the hashmap."
- State both time and space
- Don't wait to be asked
```

---

## 13. Common mistakes

### Mistake 1: Off-by-one errors
```python
# WRONG: misses last element
for i in range(len(arr) - 1):

# RIGHT: includes last element
for i in range(len(arr)):

# Range [i, j] inclusive has (j - i + 1) elements, not (j - i)
```

### Mistake 2: Modifying collection while iterating
```python
# WRONG: modifying list while looping
for item in my_list:
    if condition:
        my_list.remove(item)  # skips elements!

# RIGHT: build a new list
result = [item for item in my_list if not condition]

# RIGHT: iterate over copy
for item in my_list[:]:
    if condition:
        my_list.remove(item)
```

### Mistake 3: Integer overflow (less of an issue in Python)
```python
# Python handles big integers natively — no overflow
# But be careful with: float('inf') + float('inf') = float('inf')
# And: float('inf') - float('inf') = nan
```

### Mistake 4: Not handling empty input
```python
# Always check at the start
def my_function(nums):
    if not nums:
        return 0  # or [], or "", depending on expected output
```

### Mistake 5: Using list where you need set/dict
```python
# WRONG: O(n) lookup in list
if target in my_list:  # scans entire list

# RIGHT: O(1) lookup in set
my_set = set(my_list)
if target in my_set:   # hash-based lookup
```

### Mistake 6: Forgetting that sorted() returns a new list
```python
arr = [3, 1, 2]

arr.sort()          # modifies arr in-place, returns None
new_arr = sorted(arr)  # returns new sorted list, arr unchanged

# Common bug:
arr = arr.sort()    # arr is now None!
```

---

## 14. Cheat sheet

### Pattern recognition

```
"Find pair/triplet that..."         → Two-pointer (sort first)
"Longest/shortest subarray..."      → Sliding window
"Subarray sum equals K"             → Prefix sum + hashmap
"Most frequent / least frequent"    → Frequency counting (Counter)
"Remove/deduplicate in-place"       → Two-pointer (slow/fast)
"Do it in O(1) space"              → In-place manipulation
"Contiguous sequence"               → Sliding window or prefix sum
"Compare from both ends"            → Two-pointer (opposite)
```

### Time complexity cheat sheet

```
Hashmap/set lookup:        O(1)
Sorting:                   O(n log n)
Single loop:               O(n)
Nested loops:              O(n²) — try to eliminate inner loop
Binary search:             O(log n)
Two-pointer on sorted:     O(n)
Sliding window:            O(n)
Prefix sum build:          O(n), query: O(1)
```

### Python built-ins to know

```python
from collections import Counter, defaultdict, deque
from itertools import accumulate  # prefix sums
from heapq import heappush, heappop, nlargest, nsmallest
from bisect import bisect_left, bisect_right  # binary search

# Useful one-liners
max(arr)                    # O(n)
min(arr)                    # O(n)
sum(arr)                    # O(n)
sorted(arr)                 # O(n log n)
sorted(arr, key=lambda x: x[1])  # sort by custom key
list(zip(arr1, arr2))       # pair elements
enumerate(arr)              # (index, value) pairs
all(x > 0 for x in arr)    # check all satisfy condition
any(x > 0 for x in arr)    # check any satisfies condition
```

---

## Study plan for this section

| Day | Focus | Problems | Target |
|-----|-------|----------|--------|
| 1 | Arrays basics + Big-O | LC 1, 121, 217, 283 | Understand patterns |
| 2 | Two-pointer (opposite) | LC 11, 15, 125 | Solve without hints |
| 3 | Two-pointer (same dir) | LC 26, 283, 189 | In-place confidence |
| 4 | Sliding window (fixed) | LC 643, Moving Average | Fixed window cold |
| 5 | Sliding window (variable) | LC 3, 424 | Template memorized |
| 6 | Sliding window (hard) | LC 76, 340 | Shrink logic clear |
| 7 | Prefix sums | LC 303, 560, 525 | Prefix + hashmap combo |
| 8 | Frequency counting | LC 242, 49, 347 | Counter fluency |
| 9 | Combined patterns | LC 238, 53, 56 | Pattern recognition |
| 10 | Timed mock | Pick 3 random Medium | 30 min each, no hints |

**Daily minimum:** 2 problems. Write complexity for each. Explain solution out loud.

---

*Last updated: Phase 4, Day 1. Next: Hashmaps — the single most important data structure for infra interviews.*
