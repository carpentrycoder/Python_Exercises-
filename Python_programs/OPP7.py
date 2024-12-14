"""
def count(max_val):
    count = 1
    while count <= max_val:
        yield count
        count += 1

for number in count(5):
    print(number)

"""

class Meta(type):
    def __new__(cls, name, bases, dct):
        print(f'Creating class {name}')
        return super().__new__(cls, name, bases, dct)

class MyClass(metaclass=Meta):
    pass


import itertools

for item in itertools.chain([1, 2], ['a', 'b']):
    print(item)
