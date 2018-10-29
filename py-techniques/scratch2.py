stopwords = ['a', 'the', 'and', 'an', 'is']

test = 'this Is a tEst'.lower()

words = test.split()

words[0] = words[0].title()

for i in range(1, len(words)):
    if words[i] not in stopwords:
        words[i] = words[i].title()

print(' '.join(words))

