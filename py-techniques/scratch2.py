import math

def knapsack(nums, target):

    def ksshelp(i, T):

        if T == 0:
            return True

        if i < 0 or T < 0:
            return False

         # i in set
         # i not in set

        return ksshelp(i - 1, T - nums[i]) or ksshelp(i - 1, T)

    
    
    return ksshelp(len(nums) - 1, target)

if __name__ == '__main__':
    # execute only if run as the entry point into the program
    print(knapsack([1, 2, 5, 9, 10], 7))