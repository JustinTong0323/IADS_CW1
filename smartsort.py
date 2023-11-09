# File:    smartsort.py
# Author:  John Longley
# Date:    October 2023

# Template file for Inf2-IADS (2023-24) Coursework 1, Part A:
# Implementation of hybrid Merge Sort / Insert Sort,
# with optimization for already sorted segments.


import peekqueue
from peekqueue import PeekQueue

# Global variables


def comp(x, y): return x <= y  # comparison function used for sorting


insertSortThreshold = 10

sortedRunThreshold = 10

# TODO: Task 1. Hybrid Merge/Insert Sort

# In-place Insert Sort on A[m],...,A[n-1]:


def insertSort(A, m, n):
    # iterate over the sublist A[m+1:n]
    for i in range(m + 1, n):
        # store the current element in a variable
        v = A[i]
        j = i
        # shift elements to the right until the correct position for v is found
        while j > m and comp(v, A[j - 1]):
            A[j] = A[j - 1]
            j -= 1
        # insert v into the correct position
        A[j] = v


# Merge C[m],...,C[p-1] and C[p],...,C[n-1] into D[m],...,D[n-1]
def merge(C, D, m, p, n):
    i = m
    j = p
    k = m
    while i < p and j < n:
        # compare elements in the two subarrays
        if comp(C[i], C[j]):
            D[k] = C[i]
            i += 1
        else:
            D[k] = C[j]
            j += 1
        k += 1
    # copy remaining elements from the first subarray
    while i < p:
        D[k] = C[i]
        i += 1
        k += 1
    # copy remaining elements from the second subarray
    while j < n:
        D[k] = C[j]
        j += 1
        k += 1


# Merge Sort A[m],...,A[n-1] using just B[m],...,B[n-1] as workspace,
# deferring to Insert Sort if length <= insertSortThreshold


def greenMergeSort(A, B, m, n):
    # If the length of the list is less than or equal to insertSortThreshold, use insertion sort
    if n - m <= insertSortThreshold:
        insertSort(A, m, n)
    else:
        # Divide the list into four sublists
        q = (m + n) // 2
        p = (m + q) // 2
        r = (q + n) // 2

        # Recursively sort the sublists
        greenMergeSort(A, B, m, p)
        greenMergeSort(A, B, p, q)
        greenMergeSort(A, B, q, r)
        greenMergeSort(A, B, r, n)

        # Merge the sublists
        merge(A, B, m, p, q)
        merge(A, B, q, r, n)
        merge(B, A, m, q, n)


# Provided code:

def greenMergeSortAll(A):
    B = [None] * len(A)
    greenMergeSort(A, B, 0, len(A))
    return A


# TODO: Task 2. Detecting already sorted runs.

# Build and return queue of sorted runs of length >= sortedRunThreshold
# Queue items are pairs (i,j) where A[i],...,A[j-1] is sorted


def allSortedRuns(A):
    Q = PeekQueue()  # Initialize a PeekQueue to store sorted runs
    i = 0  # Initialize a pointer to the start of the list
    while i < len(A):
        j = i + 1
        # Find the end of the current sorted run
        while j < len(A) and comp(A[j - 1], A[j]):
            j += 1
        # If the sorted run is long enough, add it to the PeekQueue
        if j - i >= sortedRunThreshold:
            Q.push((i, j))
        i = j  # Move the pointer to the start of the next run
    return Q


# Test whether A[i],...,A[j-1] is sorted according to information in Q


def isWithinRun(Q, i, j):
    # iterate over the queue
    while Q.peek():
        # get the next pair of indices
        (a, b) = Q.peek()
        # check if the pair of indices matches the given pair
        if a > i:
            return False
        if j <= b:
            return True
        if i < b:
            break
        Q.pop()  # remove the pair of indices from the queue
    return False


# Improvement on greenMergeSort taking advantage of sorted runs

def smartMergeSort(A, B, Q, m, n):
    # If the list is already sorted, do nothing
    flag = isWithinRun(Q, m, n)
    if flag:
        # print("m:", m, "n:", n)
        return

    # If the length of the list is less than or equal to insertSortThreshold, use insertion sort\
    if n - m <= insertSortThreshold:
        insertSort(A, m, n)
    else:

        # Divide the list into four sublists
        q = (m + n) // 2
        p = (m + q) // 2
        r = (q + n) // 2

        # Recursively sort the sublists
        smartMergeSort(A, B, Q, m, p)
        smartMergeSort(A, B, Q, p, q)
        smartMergeSort(A, B, Q, q, r)
        smartMergeSort(A, B, Q, r, n)

        # Merge the sublists
        merge(A, B, m, p, q)
        merge(A, B, q, r, n)
        merge(B, A, m, q, n)


# Provided code:

def smartMergeSortAll(A):
    B = [None] * len(A)
    Q = allSortedRuns(A)
    smartMergeSort(A, B, Q, 0, len(A))
    return A


# for testing:
if __name__ == "__main__":
    # generate a list of random integers
    import random
    random.seed(323)
    A = [random.randint(0, 1000) for _ in range(1000)]
    greenMergeSort(A, [None] * 1000, 200, 900)
    # print(A)
    smartMergeSortAll(A)
    print(A)

# TODO: Task 3. Asymptotic analysis of smartMergeSortAll

""" 
1. Justification of O(n lg n) bound.
For subarrays with a length less than or equal to `insertSortThreshold`,
the algorithm uses insertion sort, which has a worst-case complexity of O(k^2) for each such subarray,
where k is the length of the subarray. However, since k is constant and does not depend on n,
the insertion sort does not affect the overall asymptotic complexity of the algorithm.
And for the `allSortedRuns` function and the subsequent checks within smartMergeSort to detect whether
a sublist is already sorted are linear operations with respect to the size of the sublist.
Therefore, the recurrence relation for `smartMergeSortAll` can be expressed as: T(n) = 4T(n/4) + Theta(n)
where the number of recursive calls is 4, subproblem factor is 4 and the time taken to merge the subproblems is Theta(n).
So by the Master Theorem, e = log_4(4) = 1, k = 1 => e = k => T(n) = Theta(n^k lg n) = Theta(n lg n) => T(n) = O(n lg n)

2. Runtime analysis for nearly-sorted inputs.
For nearly-sorted inputs where at most one item is out of place,`smartMergeSortAll` has a runtime complexity dominated by
the merge operations and thedetection of the unsorted element. The `allSortedRuns` will identify almost the entire list as sorted,
except for the segment affected by the unsorted element, which incurs a logarithmic number of comparisons to locate.
Once this element is found, as the list is nearly sorted, the `isWithinRun` function will typically return `True`,
indicating that the majority of the list does not need to be sorted, so only a constant number of linear-time merge
operations are required. Hence, the algorithm's performance is bound by O(n) for the merging and O(lg n) for locating the unsorted element.
Asymptotically, the runtime simplifies to O(n).
"""


# Functions added for automarking purposes - please don't touch these!

def set_comp(f):
    global comp
    comp = f


def set_insertSortThreshold(n):
    global insertSortThreshold
    insertSortThreshold = n


def set_sortedRunThreshold(n):
    global sortedRunThreshold
    sortedRunThreshold = n


def set_insertSort(f):
    global insertSort
    insertSort = f

# End of file
