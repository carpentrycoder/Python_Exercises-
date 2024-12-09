marks = int(input("Enter your marks: "))

if marks >= 90:
    if marks >= 95:
        print("Grade: A (Outstanding)")
    else:
        print("Grade: A")
elif marks >= 75:
    if marks >= 80:
        print("Grade: B (Very Good)")
    else:
        print("Grade: B")
elif marks >= 50:
    print("Grade: C")
else:
    print("Grade: F")
