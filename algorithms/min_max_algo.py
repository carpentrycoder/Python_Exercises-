import math

# Minimax function
def minimax(depth, nodeIndex, isMaximizingPlayer, scores, height):
    # Terminating condition: leaf node is reached
    if depth == height:
        return scores[nodeIndex]

    if isMaximizingPlayer:
        return max(minimax(depth + 1, nodeIndex * 2, False, scores, height),
                   minimax(depth + 1, nodeIndex * 2 + 1, False, scores, height))
    else:
        return min(minimax(depth + 1, nodeIndex * 2, True, scores, height),
                   minimax(depth + 1, nodeIndex * 2 + 1, True, scores, height))

# Function to validate if the number of terminal nodes is a power of 2
def is_power_of_two(n):
    return (n != 0) and (n & (n - 1) == 0)

# Driver code
if __name__ == "__main__":
    # Take user input for terminal values
    while True:
        try:
            scores = list(map(int, input("Enter the terminal node values (space-separated integers): ").split()))
            # Check if the number of scores is a power of 2
            if not is_power_of_two(len(scores)):
                raise ValueError("Number of terminal nodes must be a power of 2.")
            break
        except ValueError as e:
            print(e)
            print("Please enter a valid number of terminal node values.")

    # Height of the game tree
    height = int(math.log2(len(scores)))

    # Starting at depth 0 and the root node
    optimal_value = minimax(0, 0, True, scores, height)
    
    # Get the minimum and maximum values from the terminal node scores
    min_value = min(scores)
    max_value = max(scores)

    print("\nThe optimal value is:", optimal_value)
    print("The minimum value is:", min_value)
    print("The maximum value is:", max_value)
