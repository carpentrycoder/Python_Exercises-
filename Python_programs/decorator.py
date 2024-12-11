"""
def decorator(func):
    def wrapper():
        print("before the function call")
        func()
        print("after the function call")
    return wrapper

@decorator
def say_hello():
    print("hello")

say_hello()

"""
"""
def decorator(func):
    def wrapper(*args, **kwargs):
        print("Wrapper executed...!")
        return func(*args, **kwargs)
    return wrapper

"""

def logger(func):
    def wrapper(*args, **kwargs):
        print(f"Calling function '{func.__name__}' with arguments: {args} and{kwargs}")
        result = func(*args,**kwargs)
        print(f"Function '{func.__name__}' returned: {result}")
        return result
    return wrapper

@logger
def add(a, b):
    return a + b

@logger
def greet(name):
    return f"Hello, {name}!"

# Test the decorator
add(3, 4)  
greet("Nikhil")


