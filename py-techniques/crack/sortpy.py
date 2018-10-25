# Recursive form
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

# Iterative from
def mergeSort(arr):


#arr = list(map(int, '3 7'.split()))
arr = list(map(int, '10 9 8 7 6 5 4 3 2 1 0 -1 -2'.split()))

print(arr)
print(mergeSortR(arr))