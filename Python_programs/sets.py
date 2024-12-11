contacts = set()

contacts.add("Nikhil")
contacts.add("John")
contacts.add("Jane")

# Adding duplicate names won't work (sets ensure uniqueness)

name = input("enter a name to check: ")
if name in contacts:
    print(f"{name} exists in the contact list.")
else:
    print(f"{name} does not exist.")

print("\nAll Contacts: ")
name_to_remove = input("\nEnter a name to remove: ")
contacts.discard(name_to_remove)
print(f"\nUpdated Contacts: {contacts}")