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
