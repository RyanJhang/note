
class Solution:
    def kClosest(self, points, k: int):
        candidate = []

        for p in points:
            # s = math.sqrt(0 - p[0]) - math.sqrt(0 - p[1])
            # a^2 -ab + b^2

            candidate.append([p[0]**2 + p[1]**2, p])

        candidate.sort(key=lambda x: x[0])

        result = []
        for index in range(k):
            result.append(candidate[index][1])
        return result

    def kClosest2(self, points, k: int):

        points.sort(key=lambda point: point[0]**2 + point[1]**2)
        return points[:k]


Solution().kClosest(points=[[1, 3], [-2, 2]], k=1)
