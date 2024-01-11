import numpy as np

print("--HOW TO COPY ARRAYS USING NUM.PY --")
#shallow copy 
print()
arr1 = np.array([1,5,7,6,4])
arr2 = arr1.view() #update elment in both arrays 
print(arr1)
print(arr2)

arr1[1]=69
print(f"Shallow copied array :{arr1}")
print(f"Shallow copied array :{arr2}")
print()

#deep copy 
arr1 = np.array([1,5,7,6,4])
arr2 = arr1.copy() #update elment in only that array where we want 
arr1[1]=69
print(f"Deep copied array :{arr1}")
print(f"Deep copied array :{arr2}")

print(id(arr1))
print(id(arr2))