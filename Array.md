An array is a data structure used to store multiple values of the same type in a single variable, in an ordered way.

**Ordered Way** means elements are stored in a fixed sequence and that sequence is maintained
```python
arr = [10, 20, 30]
```
Here the order is
- index 0 -> 10
- index 1 -> 20
- index 2 -> 30

If you print:
```python
print (arr)
```
Output will always be: `[10, 20, 30]`. Order does not change automatically

### Pattern 1: Two-pointer
The idea: Instead of nested loops (O(n²)), use two pointers that move intelligently through the array — O(n).

**Variant A: Opposite direction (one at start, one at end)**
- Use when the array is sorted and you're looking for pairs.

Classic problem: Two Sum on a sorted array
- Given sorted array `[2, 7, 11, 15]` and target `9`, find two numbers that add to 9.
- Brute force: check every pair -> O(n²). Two nested loops.

Two-pointer approach:
```python
def two_sum_sorted(nums, target):
    left, right = 0, len(nums) - 1
    
    while left < right:
        total = nums[left] + nums[right]
        
        if total == target:
            return [left, right]
        elif total < target:
            left += 1      # need bigger sum
        else:
            right -= 1     # need smaller sum
    
    return []
```

Container With Most Water (LC #11, Medium)

<img width="612" height="307" alt="image" src="https://github.com/user-attachments/assets/8298f834-04d1-439c-a296-84589bc981a2" />

- Input: height = [1,8,6,2,5,4,8,3,7]
- Area = Length * Width
- And length is length is decided by minimum of left and right heights. Width will not change
- So we can only play with height
- Width keeps decreasing, so only way to improve area is by finding a taller minimum height -> move the shorter wall

```python
def max_area(height):
    left, right = 0, len(height) - 1
    best = 0
    
    while left < right:
        width = right - left
        h = min(height[left], height[right])
        best = max(best, width * h)
        
        if height[left] < height[right]:
            left += 1
        else:
            right -= 1
    
    return best
```
