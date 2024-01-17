def selection_sort(nums):
    for i in range(len(nums)):
        min_pos = i
        for j in range(i, len(nums)):
            if nums[j] < nums[min_pos]:
                min_pos = j

        nums[i], nums[min_pos] = nums[min_pos], nums[i]

user_input = input("Enter a list of numbers separated by spaces: ")
numbers = [int(x) for x in user_input.split()]
selection_sort(numbers)
print("Sorted array:", numbers)