western_menu = {
    "pizza": 3.00,
    "nachos": 4.50,
    "popcorn": 6.00,
    "fries": 2.50,
    "chips": 1.00,
    "pretzel": 3.50,
    "soda": 3.00,
    "lemonade": 4.25
}

# Indian menu
indian_menu = {
    "biryani": 8.50,
    "curry": 7.00,
    "naan": 2.50,
    "samosa": 3.00,
    "lassi": 4.50,
    "tandoori": 9.00,
    "masala chai": 2.75,
    "gulab jamun": 5.25
}

cart = []
total = 0

print("--------- MENU ---------")
print("Original Menu:")
for key, value in western_menu.items():
    print(f"{key:10}: Rs.{value:.2f}")
    print(end="")

print("\nIndian Menu:")
for key, value in indian_menu.items():
    print(f"{key:12}: Rs.{value:.2f}")
print("------------------------")

while True:
    food = input("Select an item (q to quit): ").lower()
    if food == "q":
        break
    elif western_menu.get(food) is not None:
        cart.append(food)
    elif indian_menu.get(food) is not None:
        cart.append(food)
    else:
        print("Invalid item. Please select from the menu.")

print("------ YOUR ORDER ------")
for food in cart:
    if western_menu.get(food) is not None:
        total += western_menu.get(food)
    elif indian_menu.get(food) is not None:
        total += indian_menu.get(food)
    print(food, end=" ")

print()
print(f"Total is: ${total:.2f}")