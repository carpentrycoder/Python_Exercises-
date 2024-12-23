import os
from add_transaction import add_transaction
from view_transactions import view_transactions
from generate_reports import generate_report
from visualize_data import visualize_data

def main_menu():
    while True:
        print("\n=== Personal Finance Management ===")
        print("1. Add Transaction")
        print("2. View Transactions")
        print("3. Generate Report")
        print("4. Visualize Data")
        print("5. Exit")
        choice = input("Enter your choice: ")
        print(f"DEBUG: User entered {choice}")

        if choice == '1':
            print("DEBUG: Calling add_transaction()")
            add_transaction()
        elif choice == '2':
            print("DEBUG: Calling view_transactions()")
            view_transactions()
        elif choice == '3':
            print("DEBUG: Calling generate_report()")
            generate_report()
        elif choice == '4':
            print("DEBUG: Calling visualize_data()")
            visualize_data()
        elif choice == '5':
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")
