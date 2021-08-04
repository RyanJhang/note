
class Solution:
    def maxProfit(self, prices) -> int:
        profit = 0
        for i in range( len(prices)-1 ):

            if prices[i] < prices[i+1]:
                profit += (prices[i+1]-prices[i])

        return profit

a = Solution().maxProfit([1,2,3,4,5])
print(a)
# [7,1,5,3,6,4] -> 7
# [7,6,4,3,1] -> 0