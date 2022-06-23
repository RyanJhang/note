from re import M


class Solution:
    def subsets(self, nums):
        len_nums = len(nums)
        for i in range(1 << len_nums):
            print("---", i)
            bit = i
            bin = ""
            for j in range(8):
                bin = str(bit&1) + bin
                bit = bit >> 1
                # print(bit)。
            print(bin)

    def subsets_(self, nums):
        m_len = 2**len(nums)+1
        n_len = len(nums)
        result = [[]]

        shift_list = []
        index = 0

        cur = 1
        shift = 0
        for i in range(m_len):
            if shift >= 1:
                temp = shift_list.copy()
                temp[cur-1].append(cur)
                shift_list.append(temp[cur-1])
            else:
                shift_list.append([cur])
            result.append(shift_list[-1].copy())
            # result = [[]]
            cur += 1
            if cur > n_len:
                cur = 1
                shift += 1

        a = [[], [1], [2], [1, 2], [3], [1, 3], [2, 3], [1, 2, 3]]

        # a


l = Solution().subsets([1, 2, 3])
print(l)
# 4213657
