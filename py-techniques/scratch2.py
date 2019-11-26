import math
from collections import deque

"""
Write a function that returns the elements on odd positions (0 based) in a list
"""
def solution1(input):
  # Using slicer
  #output = input[1::2]

  # Using iteration
  output = [v for i, v in enumerate(input) if i%2 == 1]

  return output


"""
Write a function that returns the cumulative sum of elements in a list
"""
def solution2(input):
    # Using built in itertools.accumulate
    runsum, tmp = [], 0

    for n in input:
      tmp += n
      runsum.append(tmp)  

    return runsum

"""
Write a function that takes a number and returns a list of its digits
"""
def solution3(input):
  # Code goes here
  output = []
  tmp = input
  
  while tmp > 0:
    
    digit = tmp%10
    output.append(digit)
    tmp //= 10

  return output[::-1]

"""
From: http://codingbat.com/prob/p126968
Return the "centered" average of an array of ints, which we'll say is 
the mean average of the values, except ignoring the largest and 
smallest values in the array. If there are multiple copies of the 
smallest value, ignore just one copy, and likewise for the largest 
value. Use int division to produce the final average. You may assume 
that the array is length 3 or more.
"""

def solution4(input):
  # Code goes here
  from functools import reduce

  # Sort input array - min and max on opposite ends
  in_order = sorted(input)
  # take the slice of array ignore first and last
  center = in_order[1:-1]
  # return average of this list

  return sum(center)//len(center) 


if __name__ == '__main__':

  assert solution1([0,1,2,3,4,5]) == [1,3,5]
  assert solution1([1,-1,2,-2]) == [-1,-2]

  assert solution2([1,1,1]) == [1,2,3]
  assert solution2([1,-1,3]) == [1,0,3]

  assert solution3(123) == [1,2,3]
  assert solution3(400) == [4,0,0]

  assert solution4([1, 2, 3, 4, 100]) == 3
  assert solution4([1, 1, 5, 5, 10, 8, 7]) == 5
  assert solution4([-10, -4, -2, -4, -2, 0]) == -3
