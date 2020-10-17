
def insertion_sort(arr):
    """
    SORT-001
    Insertion sort is good for small lists or lists that are nearly
    sorted. The optimal performance occurs when the array is already
    sorted, and arrays sorted in reverse order produce the worst
    performance for Insertion Sort. Insertion Sort requires very
    little extra space to function; it only needs to reserve space
    for a single element.

    Average: O(n^2)
    Worst: O(n^2)
    Best: O(n)

    Visualize sorting a deck of cards by taking a card from the right
    end and inserting it into its place. The only difference with this
    algorithm is that each card has a slot so when inserting, all cards
    must be shifted to the right to make room for the new card.

    :param arr: input list will be sorted in place.
    :return: None
    """
    for i in range(1, len(arr)):

        tmp = arr[i]
        ins_point = i

        for j in range(i - 1, -1, -1):
            # Shift elements > value right
            if arr[j] > tmp:
                arr[j+1] = arr[j]
                ins_point -= 1
            else:
                break

        arr[ins_point] = tmp

    return arr
