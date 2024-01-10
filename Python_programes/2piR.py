import math 

radius = float(input('enter radius of circle: '))
circumference = 2*math.pi*radius
area = math.pi*pow(radius,2)

print(f"circuference of circle {round(circumference,2)} cm  
      \n {round(area,2)}cm^2")