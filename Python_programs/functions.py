def calculator(a,b,operator):
    try:
        if operator == '+':
            return a+b
        elif operator == '-':
            return a-b
        elif operator == "*":
            return a*b
        elif operator == "/":
           if b == 0:
            return "Error: Zero isn't divisible"
           else:
            return a/b
    except Exception as e:
        return f"An error occured: {e}"
    

def fibonacci(n):
   if n <= 0:
      return "Error: Input must be a positive number"
   fib_series = [0,1]
   for i in range(2,n):
      fib_series.append(fib_series[-1]+fib_series[-2])
      return fib_series[:n]

"""

def is_palindrome(string):
   cleaned_string = string.replace("","").lower()
   return cleaned_string == cleaned_string[::-1]

string = input("enter a string to check if it's a palindrome: ")
if is_palindrome(string):
   print(f'"{string}" is a palindrome !')
else:
   print(f'"{string}" is not palindrome.')

   
def is_prime(num):
   if num <= 1:
      return False
   for i in range(2, int(num ** 0.5)+1):
      if num % i == 0:
         return False
   return True

try:
   number = int(input("enter a number to check if it's prime: "))
   if is_prime(number):
      print(f"{number} is prime number ")
   else :
      print(f"{number} is not prime number ")
except ValueError:
   print("Error")

"""

def BMICalci(w,h):
   try:
      bmi =  w / (h**2)
      if bmi < 18.5:
         category = "underweight"
      elif 18.5 <= bmi < 24.9:
         category = "normal weight"
      elif 25 <= bmi < 29.9:
         category = "Overweight"
      else:
         category = "Obesity"

      return bmi,category
   except ZeroDivisionError:
      return "error: Height can't be zero."

def factorial(n):
   if n < 0:
      return "error : facorial is not defined for negative number. "
   elif n == 0 or n==1: # base case 
      return 1
   else:    # main case 
      fact = 1
      for i in range(2,n+1):
         fact *= i
      return fact 


def alternate_case(string):
   if not string:
      return "error: input string cannot be empty. "

   result = ""
   for index, char in enumerate(string):
      if char.isaplpha():
         if index % 2 == 0:
            result += char.upper()
         else:
            result += char.lower()
      else:
         result += char
   return result

def password_validator(password):
   if len(password) < 8:
      return "Error: password must be at least "

      has_upper = any(char.isupper() for char in password)
      has_lower = any(char.islower() for char in password)
      has_digit = any(char.isdigit() for char in password)
      has_spacial = any(char in "!@#$%^&*()-_+=<>?/|}{~:" for char in password)

      if has_upper and has_lower and has_digit and has_special:
         return "Password is Strong !"
      else:
         missing = []
         if not has_upper:
            missing.append("uppercase letter")
         if not has_lower:
            missing.append("lowercase letter")
         if not has_digit:
            missing.append("special charecter")
         return f"Password is weak! Missing: {','.join(missing)}"   