def move_cars(arr):
    """
    Assumes empty space is in pos 0
    """
    #print(f"BEFORE: {arr}")
    empty_ptr, pos = 0, 1

    while pos < len(arr):
        val = arr[pos]

        if pos != val:
            # free up pos and reset ptr
            arr[empty_ptr], arr[val] = arr[val], arr[empty_ptr]

            # move val into correct pos
            arr[val], arr[pos] = arr[pos], arr[val]
            empty_ptr = pos
        
        pos += 1

    pos = len(arr)-1

    while pos >= 0:

        val = arr[pos]

        if pos != val:
            # free up pos and reset ptr
            arr[empty_ptr], arr[val] = arr[val], arr[empty_ptr]

            # move val into correct pos
            arr[val], arr[pos] = arr[pos], arr[val]
            empty_ptr = pos
        
        pos -= 1

    # Switch empty pointer
    arr[0], arr[empty_ptr] = arr[empty_ptr], arr[0]
    #print(f"AFTER: {arr}")

    return arr

if __name__ == "__main__":

    result = move_cars([0, 4, 1, 3, 2])
    assert result == [0, 1, 2, 3, 4], "Simple case"

    result = move_cars([0, 1, 3, 2])
    assert result == [0, 1, 2, 3], "Simple case 2"

    result = move_cars([0, 5, 6, 7, 4, 1, 3, 2])
    assert result == [0, 1, 2, 3, 4, 5, 6, 7], "Simple case"

    print("Success")