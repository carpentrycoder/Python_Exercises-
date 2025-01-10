import csv
import mysql.connector

# Establish the connection to MySQL
conn = mysql.connector.connect(
    host="localhost",  # Your MySQL host
    port=3306,  # Only specify the port separately if needed
    user="root",  # Your MySQL username
    password="NIKHIL2005@",  # Your MySQL password
    database="Pizzaria"  # Your MySQL database name
)

cursor = conn.cursor()

# Prepare the INSERT statement for the `staff` table
insert_query = """
    INSERT INTO staff (staff_id, first_name, last_name, position, hourly_rate)
    VALUES (%s, %s, %s, %s, %s)
"""

# Read the CSV data
data = []
with open('staff.csv', 'r', encoding='utf-8') as csvfile:
    csvreader = csv.reader(csvfile)
    next(csvreader)  # Skip the header row
    
    # Read each row from the CSV and prepare the data for insertion
    for row in csvreader:
        staff_id = row[0]
        first_name = row[1]
        last_name = row[2]
        position = row[3] if row[3] else None  # Handle NULL for position
        try:
            hourly_rate = float(row[4]) if row[4] else None  # Ensure valid decimal for hourly_rate
        except ValueError:
            hourly_rate = None  # Handle invalid hourly_rate data
        
        # Append to data list if all required values are valid
        data.append((staff_id, first_name, last_name, position, hourly_rate))

# Execute the insert for each row of data
cursor.executemany(insert_query, data)

# Commit the changes to the database
conn.commit()

# Close the connection
cursor.close()
conn.close()

print("Data inserted successfully!")
