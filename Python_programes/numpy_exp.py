import numpy as np

# Types of array declarations: array, linspace, logspace, arange, zeros, ones

print("--WE ARE THE childrens of NUMPY--")
# Array declaration
sutar1 = np.array([10, 20, 30, 40, 50])
print(f"Array: {sutar1}")

#linspace 
sutar2 = np.linspace(1,17,5)
print(f"linspace: {sutar2}")

#logspace 
sutar3 = np.logspace(1,17,5)
print(f"logspace: {sutar3}")

#arange
sutar4 = np.arange(1,46,2)
print(f"arange: {sutar4}")

#zeros 
sutar5 = np.zeros(2)
print(f"zeros: {sutar5}")

#ones
sutar6 = np.ones((6),int)
print(f"ones: {sutar6}")
