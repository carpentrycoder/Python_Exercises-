#Encapsulation

class BackAccount:
    def __init__(self,account_number,Balance):
        self.__account_number = account_number
        self.__Balance = Balance
    
    def deposit(self, amount):
        if amount > 0:
            self.__Balance -= amount
        else:
            print("invalid withdrawal amount ")

    def get_balance(self):
        return self.__Balance
    
# Abstraction 

from abc import ABC,abstractmethod

class Animal(ABC):
    @abstractmethod
    def make_sound(self):
        pass

class Dog(Animal):
    def make_sound(self):
        return "Woof !"

class Cat(Animal):
    def make_sound(self):
        return "Meow !"
        
cat = Cat()
print(cat)
