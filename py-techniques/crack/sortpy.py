from random import randint
import math

# Bubble Sort: compare each item to its neighbor and swap if
# out of order. Repeat until no swaps are necessary. Each iteration
# will swap the largest element to the end.
# Good for mostly sorted or small arrays O(n^2)
def bubbleSort(arr):
    """ In place sort """
    j = len(arr)
    while j > 0:

        swaps = 0
        # Last j elements are already sorted
        for i in range(0, j-1):
            if arr[i] > arr[i+1]:
                swaps += 1
                arr[i], arr[i+1] = arr[i+1], arr[i]

        j -= 1

        if not swaps: # no more sorting needed
            break

    return arr

# Good for mostly sorted or small arrays -O(n^2)
# Like sorting a deck of cards.
def insertionSort(arr):
    """ In place sort """
    # Traverse through 1 to len(arr) 
    for i in range(1, len(arr)): 
  
        key = arr[i] 
  
        # Move elements of arr[0..i-1], that are 
        # greater than key, to one position ahead 
        # of their current position 
        j = i-1
        while j >= 0 and key < arr[j] : 
            arr[j+1] = arr[j] 
            j -= 1

        arr[j+1] = key
        
    return arr

# Selection Sort: find the smallest item and swap it to the
# front of the array. Like sorting a deck of cards.
# Good for mostly sorted or small arrays -O(n^2)
def selectionSort(arr):
    start = 0

    while start < len(arr):
        index, small = 0, math.inf
        for i in range(start, len(arr)):
            if arr[i] < small:
                index, small = i, arr[i]

        arr[start], arr[index] = arr[index], arr[start]
        start += 1

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

    # Can reuse input array for merge
    k = pos1 = pos2 = 0

    while pos1 < len(S1) and pos2 < len(S2):
        if S1[pos1] <= S2[pos2]:
            arr[k] = S1[pos1]
            pos1 += 1
        else:
            arr[k] = S2[pos2]
            pos2 += 1

        k += 1
    
    # Only 1 element difference, at most?
    while pos1 < len(S1):
        arr[k] = S1[pos1]
        k += 1
        pos1 += 1

    while pos2 < len(S2):
        arr[k] = S2[pos2:]
        k += 1
        pos2 += 1
        
    return arr

# Recursive
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

# Function takes last element as pivot, 
# places the pivot element at its correct 
# position in sorted array, and places all 
# smaller (smaller than pivot) to left of 
# pivot and all greater elements to right 
# of pivot 
def partition(arr, low, high): 
    i = (low - 1)         # index of smaller element 
    pivot = arr[high]     # pivot 
  
    for j in range(low, high): 
  
        # If current element is smaller  
        # than or equal to pivot 
        if arr[j] <= pivot: 
          
            # increment index of 
            # smaller element 
            i += 1
            arr[i], arr[j] = arr[j], arr[i] 
        
    arr[i + 1], arr[high] = arr[high], arr[i + 1] 
    return (i + 1) 
  
def quickSortI(arr, l, h): 
    """ Iterative implementation using a stack. """  
    stack = [] 
  
    # push initial values of l and h to stack 
    stack.append(l) 
    stack.append(h) 
  
    # Keep popping from stack while is not empty 
    while stack: 
  
        # Pop h and l 
        h = stack.pop()
        l = stack.pop()
  
        # Set pivot element at its correct position in 
        # sorted array 
        p = partition(arr, l, h) 
  
        # If there are elements on left side of pivot, 
        # then push left side to stack 
        if p-1 > l: 
            stack.append(l) 
            stack.append(p - 1)
  
        # If there are elements on right side of pivot, 
        # then push right side to stack 
        if p+1 < h: 
            stack.append(p + 1)
            stack.append(h) 

def bucketSort(array, bucketSize=10):
    """ Works well when data is evenly distributed.
    """
    if len(array) == 0:
        return array

    # Determine minimum and maximum values
    minValue = min(array)
    maxValue = max(array)

    # Initialize buckets
    bucketCount = math.floor((maxValue - minValue) / bucketSize) + 1 # evenly
    buckets = [[] for _ in range(bucketCount)]

    # Distribute input array values into buckets
    for i in range(0, len(array)):
        buckets[math.floor((array[i] - minValue) / bucketSize)].append(array[i])

    # Sort buckets and place back into input array
    array = []
    for i in range(0, len(buckets)):
        buckets[i].sort()
        array.extend(buckets[i])

    return array


arr = list(map(int, '50 40 30 20 10 9 8 7 6 5 4 3 2 1'.split()))

print(arr)
#print(mergeSortR(arr))
#print(quickSort(arr))
#print(insertionSort(arr))
#print(bubbleSort(arr))
#print(selectionSort(arr))
print(bucketSort(arr))