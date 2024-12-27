def max_sum_subarray(arr, k):
    n = len(arr)
    if k > n:
        return -1
    max_sum = current_sum = sum(arr[:k])
    for i in range(k, n):
        current_sum = current_sum - arr[i-k]
        current_sum = current_sum + arr[i]
        
        if current_sum >= max_sum:
            max_sum = current_sum
    
    return max_sum
    
arr = [-1, 2, 3, -1, 4, -2, 3]
k = 2
max_sum = max_sum_subarray(arr, k)
print(max_sum)
