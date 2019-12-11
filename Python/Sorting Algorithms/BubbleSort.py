def BubbleSort(arr):
    """Sorts contents of a given list from low to high by repeatedly comparing two consecutive elements
     and swapping their position if the former is greater than the latter.

    Arguments:
            arr: List of numbers to sort
    """
    n = len(arr)
    for i in range(n):
        for j in range(n-i-1):
            if arr[j] > arr[j+1]:
                arr[j], arr[j+1] = arr[j+1], arr[j]
