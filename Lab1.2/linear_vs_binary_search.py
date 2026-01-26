import time
import random

def linear_search(arr, target):
    """Linear search: returns index of target or -1 if not found."""
    for i, val in enumerate(arr):
        if val == target:
            return i
    return -1

def binary_search(arr, target):
    low = 0
    high = len(arr) - 1

    while low <= high:
        mid = (low + high) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            low = mid + 1
        else:
            high = mid - 1
    return -1

if __name__ == "__main__":
    sizes = [10000, 50000, 100000, 200000]

    for n in sizes:
        data = list(range(n))      # sorted list from 0 to n-1
        target = n - 1             # worst-case for linear search

        # Time linear search
        start = time.time()
        linear_search(data, target)
        linear_time = time.time() - start

        # Time binary search
        start = time.time()
        binary_search(data, target)
        binary_time = time.time() - start

        print(
            f"n={n}: "
            f"Linear search time={linear_time:.5f}s, "
            f"Binary search time={binary_time:.5f}s"
        )


"""
Analysis:

1. When the input size doubles, the runtime of linear_search roughly doubles (O(n) growth).  
2. Binary_search runtime grows very slowly even when input doubles (O(log n) growth).  
3. Linear search checks elements one by one, while binary search repeatedly halves the search space, making it much faster for large lists.
"""
# Uncomment to test
# print(binary_search([1,3,5,7], 5))  # Should print 2
# print(binary_search([2,4,6,8], 5))  # Should print -1
# print(binary_search([], 10))        # Should print -1
# print(binary_search([5], 5))        # Should print 0
# print(binary_search([5], 1))        # Should print -1