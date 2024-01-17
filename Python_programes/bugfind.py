import tkinter as tk
from tkinter import scrolledtext

def check_and_run_code():
    code = code_entry.get("1.0", tk.END)

    # Try to execute the code
    try:
        exec(code)
        result_text.config(state=tk.NORMAL)
        result_text.delete("1.0", tk.END)
        result_text.insert(tk.END, "Code executed successfully!")
    except Exception as e:
        result_text.config(state=tk.NORMAL)
        result_text.delete("1.0", tk.END)
        result_text.insert(tk.END, f"Error: {str(e)}")
    finally:
        result_text.config(state=tk.DISABLED)

# Create the main window
app = tk.Tk()
app.title("Code Debugger")

# Create and place widgets
code_label = tk.Label(app, text="Enter your code:")
code_label.pack(pady=10)

code_entry = scrolledtext.ScrolledText(app, wrap=tk.WORD, width=40, height=10)
code_entry.pack(pady=10)

run_button = tk.Button(app, text="Run Code", command=check_and_run_code)
run_button.pack(pady=10)

result_text = scrolledtext.ScrolledText(app, wrap=tk.WORD, width=40, height=5, state=tk.DISABLED)
result_text.pack(pady=10)

# Start the main loop
app.mainloop()