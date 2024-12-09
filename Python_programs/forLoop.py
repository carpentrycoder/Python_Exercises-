cart = ["Apples", "Bananas", "Cherries"]
for item in cart:
    print(f"{item}")

cart = [("Apples", 20), ("Bananas", 20), ("Cherries", 100)]

total = 0 
for item,price in cart:
    print(f"- {item} and {price}")
    total = total+price

if total > 150 :
    discount = total * 0.10
    total = total - discount
else :
    print("No discount is applied")

print({total})