import csv
import os

def generate_report():
    file_path = os.path.join('data', 'transactions.csv')

    if not os.path.exists(file_path):
        print("No transactions found.")
        return

    income = 0
    expenses = 0
    category_expenses = {}

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

    savings = income - expenses

    print("\n=== Financial Report ===")
    print(f"Total Income: ${income:.2f}")
    print(f"Total Expenses: ${expenses:.2f}")
    print(f"Savings: ${savings:.2f}\n")
    print("Expenses by Category:")
    for category, amount in category_expenses.items():
        print(f"  {category}: ${amount:.2f}")
