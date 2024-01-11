import numpy as np

m1 = np.matrix('1 2 3 ; 6 5 8 ; 9 4 21')
m2 = np.matrix('4 7 7 ; 3 54 23 ; 6 4 39')

m3 = m1 + m2  
m4 = m1.dot(m2)

print(f"Addition of matrices:\n{m3}")
print(f"Multiplication of matrices:\n{m4}")