class Trie(object):
    def __init__(self, l):
        super().__init__()
        self.label = l
        self.children = []
    
    def contains(self, l):
        for n in self.children:
            if n.label == l:
                return True

        return False

    def getNode(self, l):
        for n in self.children:
            if n.label == l:
                return n

        return None

    def addWord(self, word):
        cur = self
        i = 0
        
        # Find end of Trie
        while cur.contains(word[i]):
            cur = cur.getNode(word[i])
            i += 1

        # Create chain of nodes for remaining string
        for c in word[i:]:
            cur = cur.addChild(c)

        # End all words with -1
        cur.addChild('-1')

    def addChild(self, l):
        node = Trie(l)
        self.children.append(node)
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
            return self.countWords(cur)
    
    def countWords(self, n):
        count = []
        self.countWordsR(n, count)
        return len(count)

    def countWordsR(self, n, count):
        if n.label == '-1':
            count.append(1)
        
        for c in n.children:
            self.countWordsR(c, count)

        return count

    def __str__(self):
        s = self.label

        for n in self.children:
            s += f'{n.__str__()}'

        return s

t = Trie('+')
t.addWord('hack')
t.addWord('hacker')
t.addWord('hackerrank')
t.addWord('ricardo')

print(t.find('r'))
print(t.find('zackerranks'))
print(t.find('hack'))
print(t.find('hackerrr'))