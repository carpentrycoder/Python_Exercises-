import math

# Global variable to store the total area
total_area = 0

# Function to calculate the area of a circle
def circle_area(radius):
    global total_area
    area = math.pi * radius ** 2
    total_area += area
    return area

# Function to calculate the area of a rectangle
def rectangle_area(length, width):
    global total_area
    area = length * width
    total_area += area
    return area

# Function to calculate the area of a triangle
def triangle_area(base, height):
    global total_area
    area = 0.5 * base * height
    total_area += area
    return area

# Main program
def main():
    global total_area
    print("Welcome to the Area Calculator !")

    while True:
        print("\nChoose a shape:")
        print("1. Circle")
        print("2. Rectangle")
        print("3. Triangle")
        print("4. Total Area")
        print("5. Exit")

        choice = input("Enter the number of your choice: ")

        if choice == "1":
            radius = float(input("Enter the radius of the circle: "))
            print(f"The area of the circle is: {circle_area(radius)}")
        elif choice == "2":
            length = float(input("Enter the length of the rectangle: "))
            width = float(input("Enter the width of the rectangle: "))
            print(f"The area of the rectangle is: {rectangle_area(length, width)}")
        elif choice == "3":
            base = float(input("Enter the base of the triangle: "))
            height = float(input("Enter the height of the triangle: "))
            print(f"The area of the triangle is: {triangle_area(base, height)}")
        elif choice == "4":
            print(f"\nTotal Area Calculated: {total_area}")
        elif choice == "5":
            print("Exiting the Area Calculator. Goodbye!")
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 5.")

# Run the main program
if __name__ == "__main__":
    main()