import tkinter as tk
from tkinter import ttk, messagebox

def add(x, y):
    return x + y

def subtract(x, y):
    return x - y

def multiply(x, y):
    return x * y

def divide(x, y):
    if y == 0:
        messagebox.showerror("Error", "Cannot divide by zero.")
        return None
    return x / y

def calculate():
    try:
        num1 = float(entry_num1.get())
        num2 = float(entry_num2.get())
        choice = operation_var.get()

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
                return  # Skip further processing if there was an error
            operation = "Division"

        result_label.config(text=f"{operation} result: {result}")

    except ValueError:
        messagebox.showerror("Error", "Please enter valid numbers.")

# Create the main window with a themed style
root = tk.Tk()
root.title("Modern Calculator")

# Entry widgets for input numbers
entry_num1 = ttk.Entry(root, font=('Arial', 14), justify='right')
entry_num1.grid(row=0, column=0, columnspan=4, padx=10, pady=10, sticky='nsew')

entry_num2 = ttk.Entry(root, font=('Arial', 14), justify='right')
entry_num2.grid(row=1, column=0, columnspan=4, padx=10, pady=10, sticky='nsew')

# Radio buttons for operation choices
operation_var = tk.IntVar()
operation_var.set(1)  # Default to addition

addition_radio = ttk.Radiobutton(root, text="+", variable=operation_var, value=1)
addition_radio.grid(row=2, column=0, padx=5, pady=5, sticky='nsew')

subtraction_radio = ttk.Radiobutton(root, text="-", variable=operation_var, value=2)
subtraction_radio.grid(row=2, column=1, padx=5, pady=5, sticky='nsew')

multiplication_radio = ttk.Radiobutton(root, text="*", variable=operation_var, value=3)
multiplication_radio.grid(row=2, column=2, padx=5, pady=5, sticky='nsew')

division_radio = ttk.Radiobutton(root, text="/", variable=operation_var, value=4)
division_radio.grid(row=2, column=3, padx=5, pady=5, sticky='nsew')

# Button to perform calculation
calculate_button = ttk.Button(root, text="=", command=calculate)
calculate_button.grid(row=3, column=0, columnspan=4, pady=10, sticky='nsew')

# Label to display result
result_label = ttk.Label(root, text="", font=('Arial', 14))
result_label.grid(row=4, column=0, columnspan=4, pady=10, sticky='nsew')

# Get screen width and height
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# Set window size and position to center
window_width = 400  # Set your desired window width
window_height = 500  # Set your desired window height

x_position = (screen_width - window_width) // 2
y_position = (screen_height - window_height) // 2

root.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")

# Configure row and column weights to make the GUI expandable
for i in range(5):
    root.grid_rowconfigure(i, weight=1)
    root.grid_columnconfigure(i, weight=1)

# Run the main loop
root.mainloop()