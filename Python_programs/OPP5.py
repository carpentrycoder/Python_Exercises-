#map
celcius = [0, 10, 20, 30, 40]
fahrenhiet = list(map(lambda x: (x*9/5)+32,celcius))
print(fahrenhiet)
#filter
number = [1,2,3,4,5]
odd_number = list(filter(lambda x: x % 2 != 0, number))
print(odd_number)
#reduce
from functools import reduce
product = reduce(lambda x ,y: x*y, number)
print(product)


#excercise
nums = [1,2,3,4,5,6,7,8]
sqaures = map(lambda x:x ** 2,nums)
even_sqares = list(filter(lambda x: x%2 ==0 , sqaures))
print(even_sqares)