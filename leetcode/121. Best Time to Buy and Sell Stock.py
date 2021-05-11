class Solution:
    def maxProfit(self, prices) -> int:

        f = 1000
        e = -1000
        profit = 0
        print("p e f profit")
        for p in prices:
            if profit < p - f:
                e = p
                profit = e - f
            else:
                if profit <= 0 or f - p == profit:
                    f = p
                    e = p
                    profit = e - f

            print(p, e, f, profit)

        return profit


# Solution().maxProfit([7,6,4,3,1])
# Solution().maxProfit([2,1,2,1,0,1,2])
# Solution().maxProfit([2,4,1])
Solution().maxProfit([3, 3, 5, 0, 0, 3, 1, 4])

# Input: prices = [7,1,5,3,6,4]
# Output: 5
# Explanation: Buy on day 2 (price = 1) and sell on day 5 (price = 6), profit = 6-1 = 5.
# Note that buying on day 2 and selling on day 1 is not allowed because you must buy before you sell.

# Input: prices = [7,6,4,3,1]
# Output: 0
# Explanation: In this case, no transactions are done and the max profit = 0.
