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
print(f"\n {even_sqares}")

import pandas as pd

# Sample data: product sales
data = {'Product': ['A', 'B', 'C', 'D', 'E'],
        'Sales': [150, 90, 60, 30, 20]}
df = pd.DataFrame(data)

# Sort data by sales in descending order
df = df.sort_values(by='Sales', ascending=False)

# Calculate cumulative percentage
df['Cumulative Sales'] = df['Sales'].cumsum()
df['Cumulative Percentage'] = 100 * df['Cumulative Sales'] / df['Sales'].sum()

# Identify top 20% products contributing to ~80% sales
top_products = df[df['Cumulative Percentage'] <= 80]
print(f"\n {top_products}")
