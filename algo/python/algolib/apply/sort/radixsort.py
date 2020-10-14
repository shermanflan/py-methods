

# TODO: Find the canonical implementation.
def radix_sort(arr):
    """
    2 versions
    MSD: Can start from the left
    LSD: Can start from the right (shown here)

    https://www.geeksforgeeks.org/radix-sort/

    O(n*key_size)
    """
    # Find the maximum number to know number of digits
    max1 = max(arr)  # O(n)

    # Do counting sort for every digit. Note that instead
    # of passing digit number, exp is passed. exp is 10^i
    # where i is current digit number.
    # Counting sort has to be stable for this to work.
    exp = 1
    while max1 // exp > 0:

        # This sorts array by the given exponent.
        counting_sort(arr, exp)
        exp *= 10


def counting_sort(arr, exp1):
    n = len(arr)

    # The output array elements that will have sorted arr
    output = [0] * n

    # Initialize count array for digits 0 through 9
    count = [0] * 10

    # Store count of occurrences in count[]
    for i in range(n):
        index = arr[i] // exp1  # this does a digit shift >>
        count[index % 10] += 1  # this gets the lsd

    # Change count[i] so that count[i] now contains ending
    # position of this digit in output array
    for i in range(1, 10):
        count[i] += count[i - 1]

    # Build the output array
    i = n - 1
    while i >= 0:
        index = arr[i] // exp1
        output[count[index % 10] - 1] = arr[i]
        count[index % 10] -= 1
        i -= 1

    # Copying the output array to arr[],
    # so that arr now contains sorted numbers.
    # This reuses the existing array and saves memory.
    for i in range(len(arr)):
        arr[i] = output[i]
