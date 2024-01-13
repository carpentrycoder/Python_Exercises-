import time

# Custom decorator to measure the execution time of a function
def timing_decorator(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f"{func.__name__} took {end_time - start_time:.5f} seconds to execute")
        return result
    return wrapper

# Apply the timing decorator to a function
@timing_decorator
def generate_fibonacci(limit):
    fibonacci_sequence = [0, 1]

    while fibonacci_sequence[-1] + fibonacci_sequence[-2] <= limit:
        next_fibonacci = fibonacci_sequence[-1] + fibonacci_sequence[-2]
        fibonacci_sequence.append(next_fibonacci)

    return fibonacci_sequence

# Test the decorated generate_fibonacci function
limit_input = int(input("Enter a limit for Fibonacci sequence: "))
result_sequence = generate_fibonacci(limit_input)
print(f"Fibonacci sequence up to {limit_input}: {result_sequence}")