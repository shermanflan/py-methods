from collections import deque, defaultdict, Counter
from itertools import permutations
import math
from crack.tree import BSTNode

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
  
def quickSort(arr,l,h): 
  
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
        p = partition( arr, l, h ) 
  
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

def main():
    arr = [10, 9, 8, 7, 6, 5, 4, 3, 2, 1]
    n = len(arr)
    quickSort(arr, 0, n-1)
    print(arr)

if __name__ == '__main__':
    # execute only if run as the entry point into the program
    main()