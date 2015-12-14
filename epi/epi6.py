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
