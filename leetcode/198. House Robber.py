'''
198. House Robber
Medium

You are a professional robber planning to rob houses along a street. Each house has a certain amount of money stashed, the only constraint stopping you from robbing each of them is that adjacent houses have security systems connected and it will automatically contact the police if two adjacent houses were broken into on the same night.

Given an integer array nums representing the amount of money of each house, return the maximum amount of money you can rob tonight without alerting the police.
 

Example 1:

Input: nums = [1,2,3,1]
Output: 4
Explanation: Rob house 1 (money = 1) and then rob house 3 (money = 3).
Total amount you can rob = 1 + 3 = 4.
Example 2:

Input: nums = [2,7,9,3,1]
Output: 12
Explanation: Rob house 1 (money = 2), rob house 3 (money = 9) and rob house 5 (money = 1).
Total amount you can rob = 2 + 9 + 1 = 12.
 

Constraints:

1 <= nums.length <= 100
0 <= nums[i] <= 400
--------------------------------------------------------------------
思路：
    nums = [2, 7, 9, 3, 1]
 
    i, ans
    0, 2
    1, 2 7
    2, 2 7 11
    3, 2 7 11
    4, 2 7 11 12

    當index 到哪，才計算到哪，不要先考慮後面。
    所以說
    i = 0 時，nums[0]
    i = 1 時，max(nums[0], nums[1])，所以是7
    i = 2 時，相鄰間隔要有一個空格，這時候需要考慮的狀況為 max(nums[1], nums[0] + nums[2]) = 11
    i = 3 時，這時候需要考慮的狀況為 max(nums[0] + nums[2], nums[1] + nums[3]) = 11
    由於前一個情況已經比較過 max(nums[1], nums[0] + nums[2]) = 11， 因此只需要計算 max(11, nums[1] + nums[3])
    i = 4 時，根據i = 3 的經驗，只需要比較前一個相加即可

'''


class Solution:
    def rob(self, nums: list):
        candiater = [nums[0]]
        for i in range(1, len(nums)):
            if i == 1:
                candiater.append(max(nums[i],
                                 candiater[-1]))
                continue
            elif i == 2:
                candiater.append(max(nums[i] + candiater[-2],
                                 candiater[-1]))
                continue

            candiater.append(max(nums[i] + candiater[-2],
                                 nums[i] + candiater[-3],
                                 candiater[-1]))
        return candiater[-1]

    def rob2(self, nums: list[int]):
        x = y = 0  # x: get this element, y: not get this element
        for n in nums:
            x, y = y + n, max(x, y)
            print(x, y)
        return max(x, y)


r = Solution().rob2([2, 7, 9, 3, 1])
print(r)
