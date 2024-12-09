expenses = []

def save_expenses_to_file(filename="bill.txt"):
    with open(filename,"w") as file:
        file.write("------- Expense Tracker Bill -------\n")
        if not expenses:
            file.write("No expenses recorded.\n")
        else:
            total = sum(expense["amount"] for expense in expenses)
            for i , expense in enumerate(expenses,start=1):
                file.write(
                    f"{i}. {expense['date']} - {expense['description']} - Rs.{expense['amount']}\n"
                )
            file.write("------------------------------------\n")
            file.write(f"Total Expenses: Rs.{total}\n")
            print(f"Expenses saved to {filename}.")

def add_expenses(date,description,amount,category):
    expenses.append({"date":date,"description":description,"category":category,"amount":amount})
    print(f"Expenses added: {description} of Rs.{amount} on {date}")

def view_expenses():
    #display all expenses.
    if not expenses:
        print("No expenses reloded yet !")
        return 
    print("\nRecorded Expenses: ")
    for i,expense in enumerate(expenses,start=1):
        print(f"{i}. {expense['date']} - {expense['description']} - {expense['amount']}")

def calculate_total():
    total = sum(sutar["amount"] for sutar in expenses)
    print(f"\nTotal Expenses: Rs.{total}")

def main():
        while True:
            print("\n--- Expense Tracker ---")
            print("1. Add Expense")
            print("2. View Expenses")
            print("3. Calculate Total")
            print("4. Exit")
            print("5.Save the file")
            choice = input("choose an option: ")

            if choice == "1":
                date = input("Enter date (DD/MM/YYYY): ")
                desc = input("Enter Description: ")
                amt = float(input("Enter amount: Rs."))
                category = input("Enter Category of Item:")
                add_expenses(date,desc,amt,category)
            elif choice == "2":
                view_expenses()
            elif choice == "3":
                calculate_total()
            elif choice == "4":
                print("Exiting....Goodbye!")
                break
            elif choice == "5":
                save_expenses_to_file()
            else:
                print("Invalid Choice. Please try Again...")


if __name__ == "__main__":
    main()
