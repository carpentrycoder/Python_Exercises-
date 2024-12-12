#inheritace

class Animal:
    def __init__(self,name):
        self.name = name
    
    def speak(self):
        raise NotImplementedError("Subscriber must implement abstract method")
    
class Dog(Animal):
    def speak(self):
        return f"{self.name} says woof"

class Cat(Animal):
    def speak(self):
        return f"{self.name} says Mewo!"
    
dog = Dog("Buddy")
cat = Cat("Whiskers")

print(dog.speak())
print(cat.speak())

#Composition

class Engine:
    def start(self):
        return "engine started"
    
class Car:
    def __init__(self,make,model):
        self.make = make
        self.model = model
        self.engine = Engine() # Car has an Engine

    def start(self):
            return f"{self.make} {self.model}: {self.engine.start()}"
        
car = Car("Toyota", "Fortuner")
print(car.start())