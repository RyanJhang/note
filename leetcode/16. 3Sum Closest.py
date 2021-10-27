# two pointer and greedy or binary search

class Solution:
    def threeSumClosest(self, nums: list, target: int):
        n = len(nums)
        closest = [float('inf'), 0]

        for i in range(n):
            if i + 2 < n:
                for j in range(i + 2, n):
                    count = (nums[i] + nums[i + 1] + nums[j])
                    gap = abs(target - count)
                    print(gap, target, count, "=", nums[i], nums[i + 1], nums[j])
                    if gap < closest[0]:
                        closest[0] = gap
                        closest[1] = count

        return closest[1]


# nums = [-4, -1, -1, 0, 1, 2]
nums = [1, 2, 4, 8, 16, 32, 64, 128]
r = Solution().threeSumClosest(nums, 82)
print(r)
