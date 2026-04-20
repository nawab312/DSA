**Binary Seach**

Core Idea: Instead of checking every element (linear search), you check the middle element and eliminate half the array each time.

Condition: Array must be *sorted*.

```python
def binary_search(arr, target):
    low, high = 0, len(arr) - 1

    while low <= high:
        mid = (low + high) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            low = mid + 1
        else:
            high = mid - 1

    return -1
```

### Median of Two Sorted Arrays

Given two sorted arrays nums1 and nums2 of size m and n respectively, return the median of the two sorted arrays.

The overall run time complexity should be O(log (m+n)).

```
Example 1:

Input: nums1 = [1,3], nums2 = [2]
Output: 2.00000
Explanation: merged array = [1,2,3] and median is 2.
```

```
Example 2:

Input: nums1 = [1,2], nums2 = [3,4]
Output: 2.50000
Explanation: merged array = [1,2,3,4] and median is (2 + 3) / 2 = 2.5.
```

The O(log(m+n)) constraint is the giveaway -> that immediately rules out merging arrays (which is O(m+n)). You need to binary search on the partition point.

The median splits a sorted array into two equal halves:
```
[1, 2, 3, 4]
      ↑
  left | right
 [1,2] | [3,4]
```

The rule is simple:
- max of left side ≤ min of right side
- Both halves have equal size

Now with two arrays:
- Instead of merging, you make a cut in both arrays such that together they form that same left/right split.
```
nums1 = [1, 3]
nums2 = [2, 4]

Cut nums1 after index 1 → left:[1]   right:[3]
Cut nums2 after index 1 → left:[2]   right:[4]

Combined left:  [1, 2]
Combined right: [3, 4]

max(left) = 2 ≤ min(right) = 3 -> CORRECT
```

How do you find the right cut?

You binary search the cut position in nums1. Once you fix the cut in nums1, the cut in nums2 is automatically determined (because both halves must have equal total size).
```
If nums1 has m elements, nums2 has n elements:
Total left size = (m + n + 1) / 2

Cut in nums1 = i
Cut in nums2 = total_left_size - i   ← automatic!
```

When is the cut correct?
```
nums1: [ ... maxL1 | minR1 ... ]
nums2: [ ... maxL2 | minR2 ... ]
```
Correct when:
```
maxL1 <= minR2
maxL2 <= minR1
```

```python
def findMedianSortedArrays(nums1, nums2):
    if len(nums1) > len(nums2):
        nums1, nums2 = nums2, nums1        # always search smaller array

    m, n = len(nums1), len(nums2)
    half = (m + n + 1) // 2               # left side size
    lo, hi = 0, m

    while lo <= hi:
        i = (lo + hi) // 2                # cut in nums1
        j = half - i                      # cut in nums2 (automatic)

        maxL1 = float('-inf') if i == 0 else nums1[i-1]
        minR1 = float('inf')  if i == m else nums1[i]
        maxL2 = float('-inf') if j == 0 else nums2[j-1]
        minR2 = float('inf')  if j == n else nums2[j]

        if maxL1 <= minR2 and maxL2 <= minR1:   # correct cut
            if (m + n) % 2 == 1:
                return float(max(maxL1, maxL2))
            else:
                return (max(maxL1, maxL2) + min(minR1, minR2)) / 2.0

        elif maxL1 > minR2:
            hi = i - 1                    # move cut left
        else:
            lo = i + 1                    # move cut right
```

