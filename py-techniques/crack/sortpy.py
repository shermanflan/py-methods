from random import randint

# Good for mostly sorted or small arrays -O(n^2)
def insertionSort(arr):
    L = len(arr)
    for i in range(1, L):
        j = i
        while j > 0 and arr[j] < arr[j-1]:
            arr[j], arr[j-1] = arr[j-1], arr[j]
            print(arr)
            j -= 1

    return arr

# Recursive form
# Iterative form is also possible
# O(n log n)
def mergeSortR(arr):
    if len(arr) <= 1:
        return arr

    # Divide
    mid = len(arr)//2

    # Conquer with recursion
    S1 = mergeSortR(arr[:mid])
    S2 = mergeSortR(arr[mid:])

    merge = []
    pos1 = pos2 = 0

    while pos1 < len(S1) and pos2 < len(S2):
        if S1[pos1] <= S2[pos2]:
            merge.append(S1[pos1])
            pos1 += 1
        else:
            merge.append(S2[pos2])
            pos2 += 1

    if pos1 < len(S1):
        merge.extend(S1[pos1:])
    elif pos2 < len(S2):
        merge.extend(S2[pos2:])
        
    return merge

# Recursive
# Can also be done in place, iteratively
# O(n log n)
def quickSort(arr):
    if len(arr) <= 1:
        return arr

    pivot = getPivot(arr)

    L = [n for n in arr if n < pivot]
    E = [n for n in arr if n == pivot]
    G = [n for n in arr if n > pivot]

    Lsort = quickSort(L)
    Gsort = quickSort(G)

    return Lsort + E + Gsort

def getPivot(arr):
    #p = arr[-1] # last element - not optimal for sorted lists
    p = arr[randint(0, len(arr)-1)] # randomized, closer to O(n log n)
    return p

arr = list(map(int, '10 9 8 7 6 5 4 3 2 1'.split()))

print(arr)
#print(mergeSortR(arr))
#print(quickSort(arr))
print(insertionSort(arr))