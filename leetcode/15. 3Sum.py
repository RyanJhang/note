# two pointer

class Solution:
    def threeSum(self, nums: list):
        nums.sort()
        n = len(nums)

        res = set()
        _set = set()

        for i in range(n):
            if not (i > 2 and nums[i] == nums[i - 2]):
                for j in range(i + 1, n):
                    target = -(nums[i] + nums[j])
                    if target in _set:
                        res.add((target, nums[i], nums[j]))
                _set.add(nums[i])
        return list(res)


# nums = [-4, -1, -1, 0, 1, 2]
nums = [0, 0, 0]
r = Solution().threeSum(nums)
print(r)
