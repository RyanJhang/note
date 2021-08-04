
class Solution:
    def maxProfit(self, prices) -> int:
        lower = prices[0]
        profit = 0
        for p in prices[1:]:
            lower = min(lower, p)
            profit = max(profit, p - lower)

        return profit



# a = Solution().maxProfit([7,1,5,3,6,4])

a = Solution().maxProfit([1,2,3,4,5])
print(a)
# [7,1,5,3,6,4] -> 7
# [7,6,4,3,1] -> 0