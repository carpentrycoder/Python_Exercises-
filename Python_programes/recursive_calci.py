def add(x, y):
    return x + y

def subtract(x, y):
    return x - y

def multiply(x, y):
    return x * y

def divide(x, y):
    if y == 0:
        print("Error: Cannot divide by zero.")
        return None
    return x / y

def calculator():
    while True:
        print("Recursive Calculator")
        print("1. Addition")
        print("2. Subtraction")
        print("3. Multiplication")
        print("4. Division")
        print("5. Exit")

        choice = int(input("Enter your choice (1-5): "))

        if choice == 5:
            print("Exiting the calculator. Goodbye!")
            break

        if choice < 1 or choice > 5:
            print("Invalid choice. Please enter a number between 1 and 5.")
            continue

        num1 = float(input("Enter the first number: "))
        num2 = float(input("Enter the second number: "))

        result = 0
        operation = ""

        if choice == 1:
            result = add(num1, num2)
            operation = "Addition"
        elif choice == 2:
            result = subtract(num1, num2)
            operation = "Subtraction"
        elif choice == 3:
            result = multiply(num1, num2)
            operation = "Multiplication"
        elif choice == 4:
            result = divide(num1, num2)
            if result is None:
                continue  # Skip printing result if there was an error
            operation = "Division"

        print(f"{operation} result: {result}")

calculator()