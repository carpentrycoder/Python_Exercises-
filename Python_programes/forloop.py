result = ["heads","tails","tails","heads","tails","heads","heads","tails","tails","tails"]
count = 0
for item in result:
    if item == "heads":
        count +=1

print('heads count is',{count})


for i in range(1,11):
    if i%2 == 0: 
        continue
    print(i*i)


"""
print("\nExercise 3\n")
month_list = ["January", "February", "March", "April", "May"]
expense_list = [2340, 2500, 2100, 3100, 2980]

e = input('enter expense amount')
e = int(e)

month = -1
for i in range(len(expense_list)):
    if e == expense_list[i]:
        month = i
        break

if month != -1:
    print(f'you spent {e} in this {month_list[i]}')
else :
    print(f"you didn't spent this amount {e}")

"""


"""
# 4. Lets say you are running a 5 km race. Write a program that,
#    1. Upon completing each 1 km asks you "are you tired?"
#    2. If you reply "yes" then it should break and print "you didn't finish the race"
#    3. If you reply "no" then it should continue and ask "are you tired" on every km
#    4. If you finish all 5 km then it should print congratulations message

print("\nExercise 4\n")

for i in range(8):
    print(f"you ran this {i+1} km")
    tired = input("Are you tired : Y/N")
    if(tired == "Y"):
        break
    

if (i==7):
    print("Hurry there is only one km is remaining")
else : 
    print(f"you did't finish race there is {i} km are remaining")

"""

print("\nExercise 5\n")

for i in range(1,6):
    s = ' '
    for j in range(i):
        s += '* '
    print(s)

h = 5
for i in range(1,i+1):
    print(''* (h - i)+ '*' * (2 * i - 1))


for i in range(h,0,-1):
    print(''* (h - i)+ '*' * (2 * i - 1))

for i in range(1, h + 1):
    print('*' * i)

#pyramid pattern 

for i in range(0,h):
    for j in range(0,h-i-1):
        print(end="")
    for j in range(0,i+1):
        print(chr(65+j),end=" ")
    print()

for i in range(h):
    print(" "* (h-i-1)+"* "* (i+1))
for i in range(h-1):
    print(" "* (i+1)+"* "*(h-i-1))


num =1 
for i in range (1,h+1):
    for j in range (1,i+1):
        print(num,end=" ")
        num += 1
    print()

def print_pascal_triangle(n):
     for line in range(1,n+1):
         c = 1
         for i in range(1,line+1):
             print(c,end=" ")
             c = c *(line - i) // i
         print()

print_pascal_triangle(h)