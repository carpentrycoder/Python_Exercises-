class Book:
    def __init__(self,title,author,copies):
        self.title = title
        self.author = author
        self.copies = copies

    def display_info(self):
        print(f"Title: {self.title}, Author: {self.author}, Copies Available: {self.copies}")

    def add_copies(self,count):
        self.copies += count
        Book.total_books += count
        print(f"Added {count} copies of '{self.title}'.")

    def borrow_book(self):
        if self.copies > 0:
            self.copies -= 1
            print(f"You borrowed '{self.title}'.")
        else:
            print(f"Sorry, '{self.title}' is out of stock.")
    
    def return_book(self):
        self.copies +=1
        print(f"You returned '{self.title}'.")
    
    @classmethod
    def display_total_books(cls):
        print(f"Total books in the library: {cls.total_books}")


book1 = Book("The Alchemist", "Paulo Coelho", 5)
book1.display_info()
book1.borrow_book()
book1.return_book()

