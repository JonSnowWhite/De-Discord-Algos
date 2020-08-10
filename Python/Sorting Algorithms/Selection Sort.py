def SelectionSort(arr):
    """Sorts contents of a given list from low to high by dividing the given list into a sorted and an unsorted part,
     looking for the smallest number in the unsorted part and moving it to the end of the sorted part.

    Arguments:
            arr: List of numbers to sort
    """
    n = len(arr)
    for i in range(n):
        for j in range(i+1, n):
            if arr[i] > arr[j]:
                arr[i], arr[j] = arr[j], arr[i]
