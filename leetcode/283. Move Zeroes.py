class Solution:
    def moveZeroes(self, nums: list):
        l, r = 0, 0
        while r < len(nums):
            if nums[r] != 0:
                nums[l], nums[r] = nums[r], nums[l]
                l += 1
            r += 1
        return nums

    def moveZeroes2(self, nums: list):
        k = 0

        for i in range(len(nums)):
            if nums[i] != 0:
                nums[k] = nums[i]
                k += 1
        for j in range(k, len(nums), 1):
            nums[j] = 0

        return nums

    def moveZeroes3(self, nums: list):
        k = 0
        for i, v in enumerate(nums):
            if v != 0:
                nums[i] = 0
                nums[k] = v
                k += 1

        return nums


# [0, 0, 1, 3, 12]
l = [0, 1, 0, 3, 12]
r = Solution().moveZeroes2(l)
print(r)
