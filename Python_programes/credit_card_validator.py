# Python credit card validator program

# 1. Remove any '-' or ' '
# 2. Add all digits in the odd places from right to left
# 3. Double every second digit from right to left.
#        (If result is a two-digit number,
#        add the two-digit number together to get a single digit.)
# 4. Sum the totals of steps 2 & 3
# 5. If sum is divisible by 10, the credit card # is valid

sum_odd = 0
sum_even = 0
total = 0

card_no = input("enter your credit card no.")
card_no = card_no.replace("-","")
card_no = card_no.replace(" ","")
card_no = card_no[::-1]  # this indexing operator will reverse the string 

for x in card_no[::2]:
    sum_odd += int(x)

for x in card_no[1::2]: # sum of every 2nd digit from right to left
    sum_even += int(x)*2
    if int(x) >= 10 :
        sum_even +=(1+(x%10))
    else :
        sum_even += int(x)
total = sum_even + sum_odd 
if total %10 ==0 :
    print("your Credit card is valid :(")
else:
    print("your Credit card is Invalid !!!")         
