"""
判斷 root 是否為 null，若是則回傳 0
回傳此節點的深度		
    遞迴找出 root.right 最大深度		
    遞迴找出 root.left 最大深度		
    比較兩個節點的最大深度，使用Math.Max 取 最大值		
    最後 +1，代表需要往上多加這一層
"""


# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class Solution2:
    def maxDepth(self, root: TreeNode):
        if root is None:
            return 0
        return 1 + max(self.maxDepth(root.left), self.maxDepth(root.right))


class Solution:
    def maxDepth(self, root: TreeNode):
        if not isinstance(root, TreeNode):
            return 0
        return self.get_n(0, root) + 1

    def get_n(self, n, root: TreeNode):

        if root.val is None:
            return n
        l = r = n
        if root.left is not None:
            l = self.get_n(n+1, root.left)
        if root.right is not None:
            r = self.get_n(n+1, root.right)
        return l if l >= r else r


root = TreeNode(val=3,
                left=TreeNode(val=9, left=None, right=None),
                right=TreeNode(val=20,
                               left=TreeNode(val=15, left=None, right=None),
                               right=TreeNode(val=7, left=None, right=None)))
print(Solution2().maxDepth(root))
