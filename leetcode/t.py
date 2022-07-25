class Solution:
    def threeSumClosest(self, nums: list, target: int):
        # Time Limit Exceeded
        nums.sort()
        n = len(nums)
        m, M = nums[0], nums[-1]

        # find closest to target

        candidate = []
        # if target in range(m, M):

        new_target1, v1 = self.find_closest_with_target(n, nums, target)

        nums.remove(v1)
        n = len(nums)
        new_target2, v2 = self.find_closest_with_target(n, nums, new_target1)

        nums.remove(v2)
        n = len(nums)
        k, v3 = self.find_closest_with_target(n, nums, new_target2)
        candidate = [v1, v2, v3]
        # else:
        #     if target > M:
        #         candidate.append(M)
        #     else:
        #         candidate.append(m)
        return sum(candidate)

    def find_closest_with_target(self, n, nums, target):
        buf = {}
        for i in range(n):
            buf[abs(target - nums[i])] = nums[i]
        min_k = min(buf.keys())
        return min_k, buf[min_k]

    def threeSumClosest1(self, nums: list, target: int):
        # Time Limit Exceeded
        nums.sort()
        n = len(nums)
        t = float('inf')
        out = None
        for i in range(n):
            for j in range(i + 1, n):
                for k in range(j + 1, n):
                    c = nums[i] + nums[j] + nums[k]
                    if abs(target - c) < t:
                        t = abs(target - c)
                        out = c
        return out


# n = [9, -64, -96, -41, -77, 95, 84, 85, -42, 88, -60, 84, -92, -67, -76, 6, 51, 13, 7, -55, -56, -100, 81, -76, 17, 40, -88, 21, 80, -76, 8, -39, -17, 4, 72, -75, 75, 67, -92, 10, -4, 51, -73, -36, 26, 6, 25, 93, 64, -68, -89, 29, 49, 51, 3, 14, -11, 31, 3, -69, -11, 30, 87, 80, -52, -51, 88, -35, -8, -9, -48, 86, 21, 76, -51, 87, -19, 65, 71, 21, -23, -28, 19, -14, 16, -5, 80, -55, -75, 58, -76, 19, -26, -100, 95, 86, 59, 96, 10, 72, 65, -22, 0, -79, 74, 32, 13, -77, 36, -
#      69, 62, -14, 68, -65, -51, 36, 46, 27, 0, 88, 40, 90, 37, -25, 74, 36, -81, 23, -93, 92, 57, 25, 51, -81, -56, 93, -20, 15, -14, -63, 0, 90, 81, 96, -33, -49, -81, -24, -59, -49, -5, 10, 23, -14, 32, 57, -7, -80, 58, -94, -27, 46, -49, 39, 74, 21, -96, -36, -91, -54, -94, -88, -90, 55, -7, 4, 23, 8, -19, 79, -67, 37, 31, 46, 90, -76, -77, -83, 62, -12, -19, -36, 0, -14, 23, 45, 25, -18, 21, -43, -97, -59, -14, -71, -11, 78, 33, -73, -23, 85, 11, 2, 78, -59, -50, 41, 20]
# [-100, -100, -97, -96, -96, -94, -94, -93, -92, -92, -91, -90, -89, -88, -88, -83, -81, -81, -81, -80, -79, -77, -77, -77, -76, -76, -76, -76, -76, -75, -75, -73, -73, -71, -69, -69, -68, -67, -67, -65, -64, -63, -60, -59, -59, -59, -56, -56, -55, -55, -54, -52, -51, -51, -51, -50, -49, -49, -49, -48, -43, -42, -41, -39, -36, -36, -36, -35, -33, -28, -27, -26, -25, -24, -23,
#  -23, -22, -20, -19, -19, -19, -18, -17, -14, -14, -14, -14, -14, -14, -12, -11, -11, -11, -9, -8, -7, -7, -5, -5, -
#  4, 0, 0, 0, 0, 2, 3, 3, 4, 4, 6, 6, 7, 8, 8, 9, 10, 10, 10, 11, 13, 13, 14, 15, 16, 17, 19, 19, 20, 21, 21, 21, 21, 21, 23, 23, 23, 23, 25, 25, 25, 26, 27, 29, 30, 31, 31, 32, 32, 33, 36, 36, 36, 37, 37, 39, 40, 40, 41, 45, 46, 46, 46, 49, 51, 51, 51, 51, 55, 57, 57, 58, 58, 59, 62, 62, 64, 65, 65, 67, 68, 71, 72, 72, 74, 74, 74, 75, 76, 78, 78, 79, 80, 80, 80, 81, 81, 84, 84, 85, 85, 86, 86, 87, 87, 88, 88, 88, 90, 90, 90, 92, 93, 93, 95, 95, 96,
#  96]
# t = -101
n =[0,2,1,-3]
t = 1
a = Solution().threeSumClosest(n, t)
print(a)
