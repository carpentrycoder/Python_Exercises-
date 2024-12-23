import csv
import os
import matplotlib.pyplot as plt

def visualize_data():
    file_path = os.path.join('data', 'transactions.csv')

    if not os.path.exists(file_path):
        print("No transactions found.")
        return

    category_expenses = {}
    income = 0
    expenses = 0

    with open(file_path, mode='r') as file:
        reader = csv.reader(file)
        next(reader)  # Skip the header row

        for row in reader:
            try:
                amount = float(row[1])
                category = row[2]

                if amount > 0:
                    income += amount
                else:
                    expenses += abs(amount)
                    category_expenses[category] = category_expenses.get(category, 0) + abs(amount)
            except ValueError:
                print(f"Skipping invalid transaction: {row}")

    # Generate Pie Chart for Expenses by Category
    if category_expenses:
        labels = category_expenses.keys()
        values = category_expenses.values()

        plt.figure(figsize=(8, 8))
        plt.pie(values, labels=labels, autopct='%1.1f%%', startangle=140)
        plt.title('Expenses by Category')
        plt.show()

    # Generate Bar Chart for Income vs Expenses
    plt.figure(figsize=(6, 6))
    plt.bar(['Income', 'Expenses'], [income, expenses], color=['green', 'red'])
    plt.title('Income vs Expenses')
    plt.ylabel('Amount ($)')
    plt.show()
