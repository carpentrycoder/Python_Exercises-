pos = -1
def search (list , n):
    l = 0
    u = len(list)-1
    while l <= u:
        mid = (u+l)//2
        if list[mid]==n:
            globals()['pos'] = mid
            return True
        elif list[mid]< n :
            l = mid
        else :
            u = mid

list = [1,2,5,4,7,6,8,9,3,12]
n = 3
if search (list,n):
    print("found at :",pos+1)

else:
    print("not found")    



