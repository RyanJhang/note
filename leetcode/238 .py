

class Solution:
    def productExceptSelf(self, nums: list):

        tatal = 1
        ans = []
        for index, num in enumerate(nums):
            tatal = tatal * num

        for index, num in enumerate(nums):
            ans.append(int(tatal/num))
        return ans







# Input: nums = [1,2,3,4]
# Output: [24,12,8,6]

Solution().productExceptSelf([1,2,3,4])