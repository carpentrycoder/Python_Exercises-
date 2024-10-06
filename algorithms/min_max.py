# Min-Max Algorithm in Python

def min_max(arr, depth, is_maximizing):
    if depth == len(arr):
        return 0

    if is_maximizing:
        # Maximizer's move
        best_value = float('-inf')
        for i in range(len(arr)):
            if arr[i] != None:
                # Pick one element and simulate the minimizer's move
                picked_value = arr[i]
                arr[i] = None
                value = picked_value + min_max(arr, depth + 1, False)
                arr[i] = picked_value
                best_value = max(best_value, value)
        return best_value
    else:
        # Minimizer's move
        best_value = float('inf')
        for i in range(len(arr)):
            if arr[i] != None:
                # Pick one element and simulate the maximizer's move
                picked_value = arr[i]
                arr[i] = None
                value = picked_value + min_max(arr, depth + 1, True)
                arr[i] = picked_value
                best_value = min(best_value, value)
        return best_value



# Input from the user
arr = list(map(int, input("Enter the numbers separated by space: ").split()))

max_value = max(arr)
min_value = min(arr)

# Start the Min-Max algorithm
is_maximizing = True  # Assume the first player is maximizer
result = min_max(arr, 0, is_maximizing)
print(f"Maximum value is: {max_value}")
print(f"Minimum value is: {min_value}")

print(f"The optimal result of the Min-Max algorithm is: {result}")
