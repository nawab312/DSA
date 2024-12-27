def kadane(arr):
    current_sum = max_sum = arr[0]
    for i in range(1, len(arr)):
        current_sum = max(arr[i], current_sum + arr[i])
        if current_sum >= max_sum:
            max_sum = current_sum
    return max_sum
    
arr = [-2, 1, -3, 4, -1, 2, 1, -5, 4]
max_sum = kadane(arr)

print(max_sum)
