foods = []
prices = []
total =0 

while True:
    food =input('Enter a item to BUY: (q to Quit)')
    if food.lower()=="q":
        break
    else:
        price=input(f"enter price of {food} in Rs.")
        foods.append(food)
        prices.append(price)

print("----your shopping list is ready now !!!!")
for food in foods:
    print(food, end="")

for price in prices:
    total+=price

print()
print(f"remeber take money greater than this amount Rs.{total}")    
