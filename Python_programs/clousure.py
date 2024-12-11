"""
def analyze_students():
    set_a = {"Alice", "Bob", "Charlie", "Diana"}
    set_b = {"Charlie", "Eve", "Frank", "Diana"}

    common_students = set_a & set_b
    print(f"Common stundets: {common_students}")

    only_in_a = set_a - set_b
    print(only_in_a)

    only_in_b = set_b - set_a
    print(only_in_b)

"""

"""
def outer_function(x):
    def innner_function(y):
        return x+y  #`x` is remembered from the outer function
    return innner_function

add_sum = outer_function(10)
print(add_sum(5))

"""

"""
def multiplier(factor):
    def multiply_by_factor(number):
        return factor*number
    return multiply_by_factor

fact2 = multiplier(2)
print(fact2(4))

"""

def function_tracker():
    count = 0 # Variable to track calls

    def tracker(reset = False):
        nonlocal count 
        if reset:
            count = 0  
            print("count is till zero")
        else :
            count +=1 
            print(f"function count is updatedwith {count} times")

    return tracker

track = function_tracker()

track()
track()
track(reset=True)