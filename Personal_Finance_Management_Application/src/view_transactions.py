import csv , os

def view_transactions():
    file_path = os.path.join('data','data.csv')

    if not os.path.exists(file_path):
        print("No trasactions found.")
        return
    
    with open(file_path,mode='r') as file:
        reader = csv.reader(file)
        transactions = list(reader)

    if len(transactions) <=1:
        print("No transactions found.")
        return
    
    print("\n=== Transactions ===")
    for row in transactions:
            print(f"Date: {row[0]}, Amount: {row[1]}, Category: {row[2]}, Description: {row[3]}")