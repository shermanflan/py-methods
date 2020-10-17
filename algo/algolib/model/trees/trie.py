class TrieException(Exception):
    pass


"""
Trie: An n-ary trees where each node stores a single character.
"""


# TODO: Not sure if this is a canonical implementation.
class Trie(object):

    def __init__(self, l=None):
        super().__init__()
        self.label = l
        self.nodes = {}
        self.word_count = 0

    def add(self, word):
        """

        :param word:
        :return:
        """
        if self.find(word) > 0:
            raise TrieException(f"{word} already exists.")

        cur = self

        for c in word:
            cur.word_count += 1

            if c in cur.nodes:
                cur = cur.nodes[c]
            else:
                cur.nodes[c] = Trie(c)
                cur = cur.nodes[c]

        # End all words with -1
        cur.__add('-1')

    def remove(self, word):
        if self.find(word) == 0:
            raise TrieException(f"{word} does not exist.")

        cur, i = self, 0

        for c in word:
            cur.word_count -= 1

            if cur.nodes[c].word_count == 1:
                del cur.nodes[c]
                return word
            else:
                cur = cur.nodes[c]

        if cur.is_word:
            cur.is_word = False
            return word

        return None

    def __add(self, l):
        node = Trie(l)
        self.nodes[l] = node
        self.word_count += 1
        return node

    def find(self, prefix):

        assert len(prefix) > 0, "Prefix is empty."

        cur = self

        for c in prefix:
            if c in cur.nodes:
                cur = cur.nodes[c]
            else:
                return 0

        return cur.word_count

    def find_words(self, prefix):

        assert len(prefix) > 0, "Prefix is empty."

        if self.find(prefix) == 0:
            return []

        cur = self

        for c in prefix:
            cur = cur.nodes[c]

        results = []
        self.__get_words(cur, prefix[:-1], results)

        return results

    def __get_words(self, cur, prefix, results):
        if  cur.label == '-1':
            results.append(prefix)

        for n in cur.nodes.values():
            self.__get_words(n, prefix + cur.label, results)

    def __str__(self):
        print(f'{self.label}({self.word_count})')

        for c in self.nodes.values():
            print(c.__str__(), end=' ')

        return ''
