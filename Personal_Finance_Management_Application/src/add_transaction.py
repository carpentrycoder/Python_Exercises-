import csv
import os

def add_transaction():
    date = input("enter the date (YYYY-MM-DD): ")
    amount = float(input("enter the amount: "))
    category = input("Enter the Category (e.g, Income, Food, Uitilies): ")
    description = input("Enter the Description: ")

    file_path = os.path.join('data','data.csv')
    with open(file_path,mode='a',newline='') as file:
        writer = csv.writer(file)
        writer.writerow([date,amount,category,description])

    print("Transaction added successfully.")
    