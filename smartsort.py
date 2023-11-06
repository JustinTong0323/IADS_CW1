
# File:    smartsort.py
# Author:  John Longley
# Date:    October 2023

# Template file for Inf2-IADS (2023-24) Coursework 1, Part A:
# Implementation of hybrid Merge Sort / Insert Sort,
# with optimization for already sorted segments.


import peekqueue
from peekqueue import PeekQueue

# Global variables

comp = lambda x,y: x<=y   # comparison function used for sorting

insertSortThreshold = 10

sortedRunThreshold = 10


# TODO: Task 1. Hybrid Merge/Insert Sort

# In-place Insert Sort on A[m],...,A[n-1]:

#   insertSort(A,m,n)

# Merge C[m],...,C[p-1] and C[p],...,C[n-1] into D[m],...,D[n-1]

#   merge(C,D,m,p,n)

# Merge Sort A[m],...,A[n-1] using just B[m],...,B[n-1] as workspace,
# deferring to Insert Sort if length <= insertSortThreshold

#   greenMergeSort(A,B,m,n)


# Provided code:

def greenMergeSortAll(A):
    B = [None] * len(A)
    greenMergeSort(A,B,0,len(A))
    return A


# TODO: Task 2. Detecting already sorted runs.
        
# Build and return queue of sorted runs of length >= sortedRunThreshold
# Queue items are pairs (i,j) where A[i],...,A[j-1] is sorted

#   allSortedRuns(A)

# Test whether A[i],...,A[j-1] is sorted according to information in Q

#   isWithinRun(Q,i,j)

# Improvement on greenMergeSort taking advantage of sorted runs

#   smartMergeSort(A,B,Q,m,n)


# Provided code:

def smartMergeSortAll(A):
    B = [None] * len(A)
    Q = allSortedRuns(A)
    smartMergeSort(A,B,Q,0,len(A))
    return A


# TODO: Task 3. Asymptotic analysis of smartMergeSortAll

# 1. Justification of O(n lg n) bound.
#
#
#
#
# (continue as necessary)

# 2. Runtime analysis for nearly-sorted inputs.
#
#
#
#
# (continue as necessary)


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
