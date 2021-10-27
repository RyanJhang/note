class Solution:

    def majorityElement0(self, nums: list):
        nums.sort()
        mid = int(len(nums) / 2)
        return nums[mid]

    def majorityElement1(self, nums: list):
        nums.sort()
        len_2 = int(len(nums) // 2) + 1

        if len(nums) == 1:
            return nums[0]

        for i in range(0, len_2, 1):
            if nums[i] == nums[i + len_2 - 1]:
                return nums[i]

        return ""

    def majorityElement2(self, nums):
        a = {}
        len_2 = len(nums) / 2

        if len(nums) == 1:
            return nums[0]

        for n in nums:
            if n in a:
                a[n] += 1
                if a[n] > len_2:
                    return n
            else:
                a[n] = 1
        return ""


nums = [3, 2, 3]
r = Solution().majorityElement(nums)
print(r)
