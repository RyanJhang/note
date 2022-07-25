# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


root = TreeNode(val=4,
                left=TreeNode(val=2,
                              left=TreeNode(val=1,
                                            left=None,
                                            right=None),
                              right=TreeNode(val=3,
                                             left=None,
                                             right=None)),
                right=TreeNode(val=6,
                               left=TreeNode(val=5,
                                             left=None,
                                             right=None),
                               right=TreeNode(val=7,
                                              left=None,
                                              right=None)))


class Solution:
    def preorderTraversal(self, root: TreeNode):
        out = []
        self._preorder(root, out)
        return out

    def _preorder(self, root: TreeNode, out: list):
        if root:
            out.append(root.val)
            self._preorder(root.left, out)
            self._preorder(root.right, out)

    def inorderTraversal(self, root: TreeNode):
        out = []
        self._inorder(root, out)
        return out

    def _inorder(self, root: TreeNode, out: list):
        if root:
            self._inorder(root.left, out)
            out.append(root.val)
            self._inorder(root.right, out)

    def postorderTraversal(self, root: TreeNode):
        out = []
        self._postorder(root, out)
        return out

    def _postorder(self, root: TreeNode, out: list):
        if root:
            self._postorder(root.left, out)
            self._postorder(root.right, out)
            out.append(root.val)


l = Solution().preorderTraversal(root)
print(l) 
# 4213657

l = Solution().inorderTraversal(root)
print(l)
#  1234567 

l = Solution().postorderTraversal(root)
print(l)
# 1325764