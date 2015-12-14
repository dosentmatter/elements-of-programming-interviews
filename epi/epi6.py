class P1_ThreeWayPartitioning:
    """
    Write a function that takes a list L and an index i into L, and
    rearranges the elements such that elements less than L[i] appear
    first, followed by elements equal to L[i], followed by elements
    greater than L[i]. Use O(1) space and O(|A|) time complexity.
    """

    @staticmethod
    def three_way_partition(L, i):
        """
        Partition L into the order
        [L[x] < L[i], L[x] == L[i], L[x] > L[i]]

        This works by keeping L split into 4 partitions - less than,
        equal, unknown, and greater than (in that order from low
        to high index).
        First, it puts the pivot at the 0th index. Then it starts
        looking at unknowns from the 1st index.
        Example:
        [7, X, X, X, X, X, X, X, X, X, X]
         ^  ^                          ^
         |  |                          |greater_than_end == unknown_last
         |  |
         |  |unknown_start == equals_end
         |
         |less_than_end == equals_start
        In the diagram, start means the index of the first element. last
        means the index of the last element. end means last + 1.
        The 7 is the pivot that has been placed at index 0.
        Partitions:
        less than - [0, less_than_end)
        equal - [equals_start, equals_end)
        unknown - [unknown_start, unknown_last]
        greater than - (greater_than_end, len(L) - 1]
        The greater than partition grows backwards.

        At some point, L will look like the following.
        Example:
        [0, 1, 2, 7, 7, 3, X, X, X, 9, 10]
                  ^     ^        ^
                  |     |        |greater_than_end == unknown_last
                  |     |
                  |     |unknown_start == equals_end
                  |
                  |less_than_end == equals_start

        The element at unknown_start is revealed (not and X) because this
        example is in the middle of an iteration of the while loop where
        3 is about to be swapped.

        The first unknown, 3, is less than the pivot, 7, so it gets swapped
        with the element at less_than_end. In effect, this adds to the less
        than partition and rotates the equals partition.
        Example:
        [0, 1, 2, 3, 7, 7, X, X, X, 9, 10]
                     ^     ^     ^
                     |     |     |greater_than_end == unknown_last
                     |     |
                     |     |unknown_start == equals_end
                     |
                     |less_than_end == equals_start

        The tracked indices are updated:
        less_than_end += 1
        unknown_start += 1
        unknown_start now points to an X because the iteration is done
        so the element is unknown again.

        If the next unknown is equal to the pivot it would look like the
        following.
        Example:
        [0, 1, 2, 3, 7, 7, 7, X, X, 9, 10]
                     ^     ^     ^
                     |     |     |greater_than_end == unknown_last
                     |     |
                     |     |unknown_start == equals_end
                     |
                     |less_than_end == equals_start

        In this case, we just increment unkown_start because everything
        is already in the right place.
        Example:
        [0, 1, 2, 3, 7, 7, 7, X, X, 9, 10]
                     ^        ^  ^
                     |        |  |greater_than_end == unknown_last
                     |        |
                     |        |unknown_start == equals_end
                     |
                     |less_than_end == equals_start

        If the next unknown is greater than the pivot, it would look
        like the following.
        Example:
        [0, 1, 2, 3, 7, 7, 7, 20, X, 9, 10]
                     ^        ^   ^
                     |        |   |greater_than_end == unknown_last
                     |        |
                     |        |unknown_start == equals_end
                     |
                     |less_than_end == equals_start

        The 20 gets swapped with the element at greater_than_end.
        Example:
        [0, 1, 2, 3, 7, 7, 7, X, 20, 9, 10]
                     ^        ^
                     |        |greater_than_end == unknown_last
                     |        |
                     |        |unknown_start == equals_end
                     |
                     |less_than_end == equals_start

        unknown_start stays the same because we swapped an unknown
        in its place.
        greater_than_end gets decremented because its partition
        was increased.
        In effect, this adds to the greater than partition and rotates
        the unknown partition.
        """

        if (len(L) == 0):
            return L

        pivot = L[i]

        L[0], L[i] = L[i], L[0]

        less_than_end = 0 # = equals_start
        unknown_start = 1 # = equals_end
        greater_than_end = len(L) - 1 # = unknown_last

        while(unknown_start <= greater_than_end):
            if (L[unknown_start] < pivot):
                L[unknown_start], L[less_than_end] = \
                L[less_than_end], L[unknown_start]

                unknown_start += 1
                less_than_end += 1
            elif (L[unknown_start] == pivot):
                unknown_start += 1
            else: # L[unknown_start] > pivot
                L[unknown_start], L[greater_than_end] = \
                L[greater_than_end], L[unknown_start]

                greater_than_end -= 1
