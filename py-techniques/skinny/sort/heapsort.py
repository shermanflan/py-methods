from dstruct.heap import minheap

#
# Heapsort is an implementation of selection sort using the priority queue data structure.
# O(n log n), stable
#
def heapsort(l): # inplace
    minq = minheap(l) # O(n log n)

    for i in range(len(l)):
        l[i] = minq.getmin() # O(log n)


#if __name__ == 'main':
l = [5, 4, 3, 2, 1]
heapsort(l)
print(l)