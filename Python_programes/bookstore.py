import os

class Book:
    def __init__(self, title, author, price, quantity):
        self.title = title
        self.author = author
        self.price = price
        self.quantity = quantity

    def __str__(self):
        return f"{self.title} by {self.author}, Price: ${self.price}, Quantity: {self.quantity}"

class Bookstore:
    def __init__(self, filename):
        self.filename = filename
        self.inventory = []
        self.load_inventory()

    def load_inventory(self):
     if os.path.exists(self.filename):
        with open(self.filename, 'r') as file:
            lines = file.readlines()
            for line in lines:
                # Skip empty or malformed lines
                if not line.strip():
                    continue
                try:
                    title, author, price, quantity = line.strip().split(',')
                    self.inventory.append(Book(title, author, float(price), int(quantity)))
                except ValueError:
                    print(f"Skipping malformed line: {line.strip()}")
     else:
      open(self.filename, 'w').close()


    def save_inventory(self):
        with open(self.filename, 'w') as file:
            for book in self.inventory:
                file.write(f"{book.title},{book.author},{book.price},{book.quantity}\n")

    def add_book(self, book):
        self.inventory.append(book)
        self.save_inventory()

    def view_books(self):
        if self.inventory:
            for index, book in enumerate(self.inventory, start=1):
                print(f"{index}. {book}")
        else:
            print("No books in inventory.")

    def update_book(self, index, title=None, author=None, price=None, quantity=None):
        if 0 <= index < len(self.inventory):
            book = self.inventory[index]
            if title:
                book.title = title
            if author:
                book.author = author
            if price:
                book.price = price
            if quantity:
                book.quantity = quantity
            self.save_inventory()
            print("Book updated successfully.")
        else:
            print("Invalid index.")

    def delete_book(self, index):
        if 0 <= index < len(self.inventory):
            self.inventory.pop(index)
            self.save_inventory()
            print("Book deleted successfully.")
        else:
            print("Invalid index.")

    def search_books(self, keyword):
        results = [book for book in self.inventory if keyword.lower() in book.title.lower() or keyword.lower() in book.author.lower()]
        if results:
            for book in results:
                print(book)
        else:
            print("No books found.")

def main():
    bookstore = Bookstore('inventory.txt')

    while True:
        print("\n--- Bookstore Inventory Management ---")
        print("1. Add a Book")
        print("2. View All Books")
        print("3. Update a Book")
        print("4. Delete a Book")
        print("5. Search for a Book")
        print("6. Exit")

        choice = input("Enter your choice (1-6): ")

        if choice == '1':
            title = input("Enter book title: ")
            author = input("Enter author: ")
            price = float(input("Enter price: "))
            quantity = int(input("Enter quantity: "))
            bookstore.add_book(Book(title, author, price, quantity))
            print("Book added successfully.")
        elif choice == '2':
            bookstore.view_books()
        elif choice == '3':
            index = int(input("Enter the index of the book to update: ")) - 1
            print("Leave fields blank to keep current value.")
            title = input("Enter new title: ")
            author = input("Enter new author: ")
            price = input("Enter new price: ")
            quantity = input("Enter new quantity: ")

            bookstore.update_book(
                index,
                title=title if title else None,
                author=author if author else None,
                price=float(price) if price else None,
                quantity=int(quantity) if quantity else None,
            )
        elif choice == '4':
            index = int(input("Enter the index of the book to delete: ")) - 1
            bookstore.delete_book(index)
        elif choice == '5':
            keyword = input("Enter a keyword to search for: ")
            bookstore.search_books(keyword)
        elif choice == '6':
            print("Exiting program.")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
