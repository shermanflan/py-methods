from collections import deque

class Trie(object):
    def __init__(self, l):
        super().__init__()
        self.label = l
        self.children = {}
        self.wordcount = 0
    
    def contains(self, l):
        return l in self.children

    def getNode(self, l):
        return self.children[l]

    def addWord(self, word):
        cur = self
        i = 0
        
        # Find end of Trie
        while cur.contains(word[i]):
            cur.wordcount += 1
            cur = cur.getNode(word[i])
            i += 1

        # Create chain of nodes for remaining string
        for c in word[i:]:
            cur = cur.addChild(c)

        # End all words with -1
        cur.addChild('-1')

    def addChild(self, l):
        node = Trie(l)
        self.children[l] = node
        self.wordcount += 1
        return node

    def find(self, p):
        cur = self
        i = 0

        while i < len(p) and cur.contains(p[i]):
            cur = cur.getNode(p[i])
            i += 1

        if i == 0 or i < len(p):
            return 0 # no prefix
        else:
            return cur.wordcount

    def __str__(self):
        print(f'{self.label}({self.wordcount})')

        for c in self.children.values():
            print(c.__str__(), end=' ')

        return ''

def contacts(queries):
    book = Trie('root')
    counts = []
    
    for q in queries:
        cmd, arg = q[0], q[1]
        
        if cmd == 'add':
            book.addWord(arg)
        elif cmd == 'find':
            found = book.find(arg)
            counts.append(found)
        else:
            raise Exception('Invalid command!')
    
    return counts

try:

    with open("C:\\Users\\rguzman\\Desktop\\test.txt", "r", encoding="utf-8") as f:

        queries_rows = int(f.readline().rstrip())
        queries = []

        for _ in range(queries_rows):
            queries.append(f.readline().rstrip().split())

        result = contacts(queries)
        print('\n'.join(map(str, result)))

except Exception as e:
    print(e)