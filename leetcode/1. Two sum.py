class Solution:
    def twoSum(self, nums: list, target: int):
        candidate = {}
        for index, value in enumerate(nums):
            if value in candidate:
                return candidate[value], index
            else:
                candidate[target - value] = index


r = Solution().twoSum([2, 7, 11, 15], 9)
print(r)
