import bisect # assumes a sorted list is used

c = [1, 2, 2, 2, 3, 4, 7]

# Binary search: where to insert 2?
print(bisect.bisect(c, 2))

# Binary search: where to insert 5?
print(bisect.bisect(c, 5))

# Binary search: inserts 6
bisect.insort(c, 6)
print(c)