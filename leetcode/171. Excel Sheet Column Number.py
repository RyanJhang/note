"""
從範例可以知道 
A = 1
AA = 27 -> 26*1 + 1
AAA = 703 -> 26*26*1 + 26*1 + 1

所以可以發現到會存在一個次方關係

以ABC舉例，逐一推導

1*26*26 + 2*26 + 3

A * 26 ** 2 + B * 26 ** 1 + C * 26 ** 0

A * 26 ** (位數 - 1) + B * 26 ** (位數 - 1) + C * 26 ** (位數 - 1)
我們會發現變動的是 位數和ABC，因此改成for的時候會發現，是從0開始的，因此執行for之前，先取得字串長度。

如此我們就得到答案囉

此外程式碼中，是用Mapping的方式，其實後來發現用ord也是可以的喔，但要記得 ord('A') - ord('A') + 1 基準點才是從1開始喔
"""


class Solution:
    def titleToNumber(self, columnTitle: str):
        mapping = {"A": 1,
                   "B": 2,
                   "C": 3,
                   "D": 4,
                   "E": 5,
                   "F": 6,
                   "G": 7,
                   "H": 8,
                   "I": 9,
                   "J": 10,
                   "K": 11,
                   "L": 12,
                   "M": 13,
                   "N": 14,
                   "O": 15,
                   "P": 16,
                   "Q": 17,
                   "R": 18,
                   "S": 19,
                   "T": 20,
                   "U": 21,
                   "V": 22,
                   "W": 23,
                   "X": 24,
                   "Y": 25,
                   "Z": 26}
        sum = 0
        l = len(columnTitle)
        for s in columnTitle:
            l -= 1
            sum += mapping[s] * 26**(l)
        return sum


sum = Solution().titleToNumber("AAA")

print(sum)
