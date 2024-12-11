def contact_manager():
    contacts = {}

    def add_contacts(name, number):
        contacts[name] = number
        print(f"added {name} with number {number}.")

    def delete_contact(name):
        if name in contacts:
            contacts.pop(name)
            print(f"this number is deleted {name}...")
        else:
            print(f"this guy({name}) is not found...")

    def search_contact(name):
        if name in contacts:
            print(f"this number is found here {name}...")
        else:
            print(f"this guy({name}) is not found...")

    def view_contacts():
        if contacts:
            print("\nAll Contacts:")
            for name, number in contacts.items():
                print(f"{name}: {number}")
        else:
            print("No contacts available.")

 
        def menu():
            while True:
                print("\n--- Contact Manager ---")
                print("1. Add Contact")
                print("2. Delete Contact")
                print("3. Search Contact")
                print("4. View All Contacts")
                print("5. Exit")

                choice = input("Choose an option: ")

                if choice == "1":
                    name = input("Enter name: ")
                    number = input("Enter number: ")
                    add_contacts(name, number)
                elif choice == "2":
                    name = input("Enter name to delete: ")
                    delete_contact(name)
                elif choice == "3":
                    name = input("Enter name to search: ")
                    search_contact(name)
                elif choice == "4":
                    view_contacts()
                elif choice == "5":
                    print("Exiting...")
                    break
                else:
                    print("Invalid choice. Please try again.")

                menu()

