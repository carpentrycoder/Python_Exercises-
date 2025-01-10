import pandas as pd
from faker import Faker
import random
import getindianname as name

# Initialize Faker with Indian locale
fake = Faker('en_IN')

# Generate data for customers table
def generate_customers(num_records):
    customers = []
    for i in range(num_records):
        # Randomly choose between male, female, or general random name
        full_name = random.choice([name.randname(), name.male(), name.female()])
        first_name, last_name = full_name.split(' ', 1)  # Split into first and last names
        customers.append({
            'cust_id': i + 1,  # Assuming cust_id is auto-incremented
            'cust_firstname': first_name,
            'cust_lastname': last_name
        })
    return pd.DataFrame(customers)

# Generate data for address table
def generate_addresses(num_records):
    localities = ['Mumbai', 'Bandra', 'Thane', 'Andheri', 'Navi Mumbai']
    addresses = []
    for i in range(num_records):
        addresses.append({
            'add_id': i + 1,  # Assuming add_id is auto-incremented
            'delivery_address1': fake.building_number(),
            'delivery_address2': fake.street_address(),
            'delivery_city': random.choice(localities),
            'delivery_zipcode': fake.postcode()
        })
    return pd.DataFrame(addresses)

# Generate data for item table
def generate_items(num_records):
    items = []
    categories = ['Pizza', 'Pasta', 'Salad', 'Dessert']
    sizes = ['Small', 'Medium', 'Large']
    for i in range(num_records):
        items.append({
            'item_id': i + 1,  # Assuming item_id is auto-incremented
            'sku': fake.unique.ean(length=8),
            'item_name': fake.word().capitalize(),
            'item_cat': random.choice(categories),
            'item_size': random.choice(sizes),
            'item_price': round(random.uniform(300.0, 1500.0), 2)  # Prices in INR
        })
    return pd.DataFrame(items)

# Generate data for orders table
def generate_orders(num_records, num_customers, num_addresses, num_items):
    orders = []
    for i in range(num_records):
        orders.append({
            'row_id': i + 1,  # Assuming row_id is auto-incremented
            'order_id': fake.unique.uuid4()[:8],  # Shortened UUID for simplicity
            'created_at': fake.date_time_this_year(),
            'item_id': random.randint(1, num_items),
            'quantity': random.randint(1, 5),
            'cust_id': random.randint(1, num_customers),
            'delivery': fake.boolean(),
            'add_id': random.randint(1, num_addresses)
        })
    return pd.DataFrame(orders)

# Generate data for ingredient table with actual pizza ingredients
def generate_ingredients(num_records):
    ingredients = []
    pizza_ingredients = [
        'Mozzarella Cheese', 'Cheddar Cheese', 'Parmesan Cheese', 'Pepperoni', 'Sausage',
        'Mushrooms', 'Onions', 'Bell Peppers', 'Olives', 'Tomato', 'Basil', 'Garlic',
        'Pineapple', 'Ham', 'Chicken', 'Bacon', 'Spinach', 'Feta Cheese', 'Ricotta Cheese',
        'Anchovies', 'Artichokes', 'Sun-dried Tomatoes', 'Arugula', 'Barbecue Sauce', 'Pesto'
    ]
    
    for i in range(num_records):
        ingredient_name = random.choice(pizza_ingredients)
        ingredients.append({
            'ing_id': i + 1,  # Assuming ing_id is auto-incremented
            'ing_name': ingredient_name,
            'ing_weight': round(random.uniform(50.0, 500.0), 2),  # Weight in grams
            'ing_meas': random.choice(['g', 'kg', 'ml', 'L']),  # Measurement units
            'ing_price': round(random.uniform(10.0, 200.0), 2)  # Price in INR
        })
    
    return pd.DataFrame(ingredients)

# Generate data for recipes table
def generate_recipes(num_records, num_ingredients):
    recipes = []
    for i in range(num_records):
        recipes.append({
            'row_id': i + 1,  # Assuming row_id is auto-incremented
            'recipe_id': fake.unique.uuid4()[:8],  # Unique Recipe ID
            'ing_id': random.randint(1, num_ingredients),
            'quantity': random.randint(50, 500)  # Quantity in grams or milliliters
        })
    return pd.DataFrame(recipes)

# Generate data for staff table with fewer staff members
def generate_staff(num_records):
    staff = []
    for i in range(num_records):
        first_name = name.randname().split()[0]
        last_name = name.randname().split()[1]
        staff.append({
            'staff_id': i + 1,  # Now only creating a few staff records
            'first_name': first_name,
            'last_name': last_name,
            'position': random.choice(['Chef', 'Waiter', 'Manager', 'Cleaner']),
            'hourly_rate': round(random.uniform(100.0, 800.0), 2)  # Hourly rate in INR
        })
    return pd.DataFrame(staff)

# Generate data for shifts table (keeping 1000 records)
def generate_shifts(num_records):
    shifts = []
    for i in range(num_records):
        shifts.append({
            'shift_id': fake.unique.uuid4()[:8],  # Unique Shift ID
            'day_of_week': random.choice(['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']),
            'start_time': fake.time(),
            'end_time': fake.time()
        })
    return pd.DataFrame(shifts)

# Generate data for rota table with fewer staff references
def generate_rota(num_records, num_shifts, num_staff):
    rota = []
    for i in range(num_records):
        rota.append({
            'row_id': i + 1,  # Assuming row_id is auto-incremented
            'rota_id': fake.unique.uuid4()[:8],  # Unique Rota ID
            'date': fake.date_this_year(),
            'shift_id': random.choice(range(1, num_shifts + 1)),
            'staff_id': random.choice(range(1, num_staff + 1))  # Ensure staff_id is within the reduced staff range
        })
    return pd.DataFrame(rota)

# Generate data for inventory table
def generate_inventory(num_records, num_items):
    inventory = []
    for i in range(num_records):
        inventory.append({
            'inv_id': i + 1,  # Assuming inv_id is auto-incremented
            'item_id': random.randint(1, num_items),
            'quantity': random.randint(50, 200)  # Quantity in stock
        })
    return pd.DataFrame(inventory)

# Adjust number of staff records to 100 instead of 1000
num_staff_records = 100
num_records = 1000  # Adjust the number of records for other tables

# Generate datasets
ingredients_df = generate_ingredients(num_records)
recipes_df = generate_recipes(num_records, num_records)  # Assuming num_ingredients is the same as num_records
inventory_df = generate_inventory(num_records, num_records)  # Assuming num_items is the same as num_records
staff_df = generate_staff(num_staff_records)  # Reduced number of staff
shifts_df = generate_shifts(num_records)
rota_df = generate_rota(num_records, num_records, num_staff_records)  # Adjusted for reduced staff
customers_df = generate_customers(num_records)
addresses_df = generate_addresses(num_records)
items_df = generate_items(num_records)
orders_df = generate_orders(num_records, num_records, num_records, num_records)

# Export to CSV
# Handle non-UTF-8 characters by ignoring or replacing them
ingredients_df.to_csv('ingredients.csv', index=False, encoding='utf-8', errors='ignore')
recipes_df.to_csv('recipes.csv', index=False, encoding='utf-8', errors='ignore')
inventory_df.to_csv('inventory.csv', index=False, encoding='utf-8', errors='ignore')
staff_df.to_csv('staff.csv', index=False, encoding='utf-8', errors='ignore')
shifts_df.to_csv('shifts.csv', index=False, encoding='utf-8', errors='ignore')
rota_df.to_csv('rota.csv', index=False, encoding='utf-8', errors='ignore')
# Handle non-UTF-8 characters by ignoring or replacing them
customers_df.to_csv('customers.csv', index=False, encoding='utf-8', errors='ignore')
addresses_df.to_csv('addresses.csv', index=False, encoding='utf-8', errors='ignore')
items_df.to_csv('items.csv', index=False, encoding='utf-8', errors='ignore')
orders_df.to_csv('orders.csv', index=False, encoding='utf-8', errors='ignore')
