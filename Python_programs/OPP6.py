"""
try:
    result = 10/0
except ZeroDivisionError:
    print("Cannot divide by zero.")
else:
     print("Division successful.")
finally:
     print("Operation Complete.")
"""

#file handling :
"""
file = open('bill.txt','r') 
with open('bill.txt','w') as file:
    file.write("Sutar !")

print(file.read())
"""

try:
    with open('rare.txt','r') as file:
        content = file.read()
except FileNotFoundError:
    print("The file does not exist.")



