item= input("What would you like to buy ? ")
price = float(input("enter price : \n"))
Quantity = int(input("enter Qunatity : \n"))
total = price*Quantity
total=int(total)

print(f"you hav bought {Quantity} X {item}\s")
print(f"your total is :{round(total,2)} Rs")