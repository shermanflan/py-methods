

class TreeNode(object):
    """ """
    def __init__(self, name):
        super().__init__()

        self.name = name
        self.left = None
        self.right = None
    
    def __repr__(self):
        return f'{self.name}'

    @staticmethod
    def allSequences(node):
        """
        TODO: Use a deque
        """
        results = []

        if not node:
            return results

        prefix = []
        prefix.append(node.name)

        leftSeq = TreeNode.allSequences(node.left)
        rightSeq = TreeNode.allSequences(node.right)

        for left in leftSeq:
            for right in rightSeq:
                weaved = []


    @staticmethod
    def weaveLists(first, second, results, prefix):

        if not first or not second:
            result = prefix[:]
            result.extend(first)
            result.extend(second)
            results.append(result)
            return

        headFirst = first.pop(0)
        prefix.append(headFirst)
        TreeNode.weaveLists(first, second, results, prefix)
        prefix.pop()
        first.insert(0, headFirst)

        headSecond = second.pop(0)
        prefix.append(headSecond)
        TreeNode.weaveLists(first, second, results, prefix)
        prefix.pop()
        second.insert(0, headSecond)

    @staticmethod
    def buildTree(nodes):
        if not nodes:
            return

        ix = len(nodes)//2
        root = TreeNode(nodes[ix])
        root.left = TreeNode.buildTree(nodes[:ix])
        root.right = TreeNode.buildTree(nodes[ix + 1:])

        return root

nodes = [5, 10, 15, 20, 25, 50, 60, 65, 70, 80, 85]
bst = TreeNode.buildTree(nodes)

first = [1, 2]
second = [3, 4]

TreeNode.weaveLists(first, second, results, prefix)

print(f'{results}')

