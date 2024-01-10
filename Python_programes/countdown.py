import time

my_time = int(input('enter time in seconds : '))

for x in reversed(range(my_time)):
    sec = int(x%60)
    min = int((x/60)%60)
    hrs = int(x / 3600)
    print(f"{hrs:02}:{min:02}:{sec:02}")
    time.sleep(1)

print("times up SUTAR !!!")
