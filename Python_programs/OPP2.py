class BankAccount:
    bank_name = "DNS Bank"

    def __init__(self,account_number,account_holder,balance=0):
        self.account_number = account_number
        self.account_holder = account_holder
        self.balance = balance
        self.trasaction_history = [] # List to store transaction details

    def deposit(self,amount):
        if amount > 0:
            self.balance += amount
            self.trasaction_history.append(f"Deposited Rs.{amount}")
            print(f"Rs.{amount} deposited successfully. new balance: {self.balance}")
        else:
            print("Invalid deposit amount.")

    def withdraw(self,amount):
        if 0 < amount <= self.balance:
            self.balance -= amount
            self.transaction_history.append(f"withdraw :Rs.{amount}")
            print(f"₹{amount} withdrawn successfully. New balance: ₹{self.balance}")
        elif amount > self.balance :
            print("Insufficient Balance")
        else:
            print("Invalid withdrawal amount.")

    
