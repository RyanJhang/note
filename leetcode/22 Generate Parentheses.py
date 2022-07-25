class Solution:
    def generateParenthesis_recusive(self, n: int):

        def recusive(self, cs, n, r, l):
            if r == l == n:
                self.result.append(cs)
            else:
                if r < n:
                    recusive(self, cs+"(", n, r+1, l)
                if l < r:
                    recusive(self, cs+")", n, r, l+1)
        self.result = []
        recusive(self, "", n, 0, 0)

        return self.result

    def generateParenthesis_set(self, n: int):
        res = ["()"]
        for _ in range(1, n):
            _temp = []
            for s in res:
                s_list = [i for i in s]
                s_temp = []

                for i in range(len(s_list)):
                    temp = s_list.copy()
                    temp.insert(i, '()')
                    tt = ''.join(temp)
                    s_temp.append(tt)
                _temp.extend(s_temp)
            res = set(_temp)

        return res


a = Solution().generateParenthesis_recusive(4)
a
