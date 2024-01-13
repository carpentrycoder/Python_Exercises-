from functools import reduce

# Task 1: User input for the list of numbers
numbers_str = input("Enter a list of numbers separated by spaces: ")
numbers = list(map(int, numbers_str.split()))

# Task 2: Filtering - Even Numbers
even_numbers = list(filter(lambda x: x % 2 == 0, numbers))

# Task 3: Mapping - Square of Numbers
squared_numbers = list(map(lambda x: x**2, numbers))

# Task 4: Reducing - Product of Numbers
product_of_numbers = reduce(lambda x, y: x * y, numbers)

# Print the results
print("Original Numbers:", numbers)
print("Even Numbers:", even_numbers)
print("Squared Numbers:", squared_numbers)
print("Product of Numbers:", product_of_numbers)