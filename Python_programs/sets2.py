# Create two sets
friends = {"John", "Jane", "Alice"}
family = {"Jane", "Bob", "Alice", "Nikhil"}

all_contacts = friends.union(family)
print("Union of friends and family (All contacts): ")
print(all_contacts)

common_contacts = friends.intersection(family)
print(common_contacts)

print(f"\nTotal Unique Contacts: {len(all_contacts)}")


import getindianname
print(dir(getindianname))
