pos = -1

def search(lst, target):
    i = 0
    while i < len(lst):
        if lst[i] == target:
            globals()['pos'] = i
            return True
        i = i + 1
    return False

# Take the list and n from the user
user_list = input("Enter a list of numbers (comma-separated): ")
user_list = [int(x) for x in user_list.split(",")]

user_n = int(input("Enter the number to search for: "))

if search(user_list, user_n):
    print("Found at position:", pos)
else:
    print("Not found")     

    