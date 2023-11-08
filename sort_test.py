import unittest
from smartsort import *
from peekqueue import *
import random

class TestSmartSort(unittest.TestCase):

    def test_insertSort(self):
        a = list(range(100, 1, -1))
        insertSort(a, 0, len(a))
        self.assertEqual(a, sorted(a))

    def test_merge(self):
        a = list(range(1, 100, 2))
        b = list(range(2, 100, 2))
        c = a + b
        b = [0] * len(c)
        merge(c, b, 0, len(a), len(c))
        self.assertEqual(b, list(range(1, 100)))

    def test_greenMergeSort(self):
        a = list(range(100, 1, -1))
        b = [0] * len(a)
        greenMergeSort(a, b, 0, len(a))
        self.assertEqual(a, sorted(a))

    def test_greenMergeSortAll(self):
        a = list(range(1000, 1, -1))
        greenMergeSortAll(a)
        self.assertEqual(a, sorted(a))

    def test_allSortedRuns(self):
        cases = [
            ([5, 2, 3, 3, 4, 1, 10, 8, 11, 12], 3, [(1, 5), (7, 10)]),
            ([1, 2, 3, 4, 5], 3, [(0, 5)]),
            ([5, 4, 3, 2, 1], 1, [(0, 1), (1, 2), (2, 3), (3, 4), (4, 5)]),
            ([1], 1, [(0, 1)])
        ]
        for a, threshold, expected in cases:
            with self.subTest(a=a, threshold=threshold):
                set_sortedRunThreshold(threshold)
                self.assertEqual(queueToList(allSortedRuns(a)), expected)

    def test_peekQueue(self):
        Q1 = PeekQueue()
        Q1.push((1, 5))
        Q1.push((7, 10))
        self.assertTrue(isWithinRun(Q1, 1, 5))
        self.assertTrue(isWithinRun(Q1, 2, 5))
        self.assertFalse(isWithinRun(Q1, 0, 5))
        self.assertFalse(isWithinRun(Q1, 1, 6))
        # Additional tests can be added following the same pattern

    def test_largeSmartMergeSort(self):
        a = list(range(1000000, 1, -1))
        random.shuffle(a)
        smartMergeSortAll(a)
        self.assertEqual(a, sorted(a))

if __name__ == '__main__':
    unittest.main()

