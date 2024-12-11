contacts = {}

contacts["nikhil"] = "7738544966"
contacts["sahil"] = "1566334545"

def add_contact(name,number):
    contacts.update({name:number})

def delete_contact(name):
    contacts.pop(name)

def search():
    name = input("enter name to search: ")
    if name in contacts:
        print(f"{name}'s contact number is {contacts[name]}")
    else:
        print("Contact not found.")

def view_contacts():
        if contacts:
            print("\nAll Contacts:")
            for name, number in contacts.items():
                print(f"{name}: {number}")
        else:
             print("no contact avalible")

def main():
     while True:
            print("\n--- Contact Manager ---")
            print("1. Add Contact")
            print("2. Delete Contact")
            print("3. Search Contact")
            print("4. View All Contacts")
            print("5. Exit")

            choice = input("Choose an option: ")

            if choice == "1":
                 name = input("enter name: ")
                 number = input("Enter your contact number")
                 add_contact(name, number)
            elif choice == "2":
                 name = input("Enter name to delete: ")
                 delete_contact(name)
            elif choice == "3":
                 search()
            elif choice == "4":
                 view_contacts()
            elif choice == "5":
                 print("exiting code bye bye !")
                 break
            else:
                 print("invalid choice ,  please try again")


if __name__ == "__main__":
     main()