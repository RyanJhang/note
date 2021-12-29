class Solution:
    def find_duplcat2(self, strs: list):
        strs.sort()
        prefix = ''
        for a, b in zip(strs[0], strs[-1]):
            if a != b:
                break
            prefix += a
        return prefix

    def find_duplcat1(self, strs: list):
        min_str = 'x' * 201
        for word in strs:
            if len(word) < len(min_str):
                min_str = word
        len_min_str = len(min_str)

        max_str = ''
        for word in strs:
            if len(word) < len(max_str):
                max_str = word
        len_max_str = len(max_str)

        candidate = {}
        for iter in range(1, len_min_str):
            s = 0
            e = iter
            for i in range(0, len_min_str, 1):
                if e + i <= len_min_str:
                    candidate_word = min_str[s + i:e + i]
                    print(candidate_word)
                    for word in strs:
                        if candidate_word in word and candidate_word in candidate:
                            candidate[candidate_word] += 1
                        else:
                            candidate[candidate_word] = 1
        return candidate

# ["fr", "twfiser", "dggfiser", "gggfiser"]
r = Solution().find_duplcat2(["flower","flow","flight"])
print(r)
