class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def display_info(self):
        print(f"Name: {self.name}, Age: {self.age}")


class Employee(Person):
    def __init__(self, name, age, employee_id):
        super().__init__(name, age)
        self.employee_id = employee_id

    def display_info(self):
        super().display_info()
        print(f"Employee ID: {self.employee_id}")


class Manager(Employee):
    def __init__(self, name, age, employee_id, department):
        super().__init__(name, age, employee_id)
        self.department = department

    def display_info(self):
        super().display_info()
        print(f"Department: {self.department}")


# Example usage
person1 = Person("John Doe", 30)
person1.display_info()

print("\n")

employee1 = Employee("Jane Smith", 25, "E12345")
employee1.display_info()

print("\n")

manager1 = Manager("Alice Johnson", 35, "M67890", "Human Resources")
manager1.display_info()