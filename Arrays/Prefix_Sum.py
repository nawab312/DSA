def compute_prefix_sum(arr):
    prefix_sum = [0]*len(arr)
    prefix_sum[0] = arr[0]
    
    for i in range(1, len(arr)):
        prefix_sum[i] = prefix_sum[i - 1] + arr[i]
    return prefix_sum

# Example Usage    
arr = [1, 2, 3, 4, 5]
prefix = compute_prefix_sum(arr)
print(prefix)
# Output: [1, 3, 6, 10, 15]

#Query sum of Subarray [1, 3]
l, r = 1, 3
subarray_sum = prefix[r] - prefix[l - 1]

print(f"Subararray Sum [1,3]: {subarray_sum}")
#Output: Subararray Sum [1,3]: 9
