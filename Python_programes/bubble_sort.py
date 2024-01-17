def sort(nums):
    for i in range(len(nums) - 1, 0, -1):
        for j in range(i):
            if nums[j] > nums[j+1]:
                temp = nums[j]
                nums[j] = nums[j+1]
                nums[j+1] = temp


nums_str = input("Enter a list of numbers separated by spaces: ")
nums = [int(x) for x in nums_str.split()]
sort(nums)
print("Sorted list:", nums)