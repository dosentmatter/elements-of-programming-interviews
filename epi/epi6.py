from epi.utils import listextra

class P1_ThreeWayPartitioning:
    """
    Write a function that takes a list L and an index i into L, and
    rearranges the elements such that elements less than L[i] appear
    first, followed by elements equal to L[i], followed by elements
    greater than L[i]. Use O(1) space and O(|L|) time complexity.
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

        In this case, we just increment unknown_start because everything
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

        It is also possible to not swap the pivot with the 0th index element
        at the start. Then unknown_start = 0 in the beginning instead of 1.
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

class P1_1_ThreeKeyPartitioning:
    """
    Keys take one of three values. Reorder L so that all objects of the
    same key appear in the same subarray. The order of the subarrays is
    not important. Use O(1) space and O(|L|) time complexity.
    """

    @staticmethod
    def three_key_partition(L):
        """
        Reorder L so that all objects of the same key appear in the same
        subarray. The order of the subarrays is the order that the key
        values are seen. Use O(1) space and O(|L|) time complexity.
        Keys take one of three values.

        This works the same as three_way_partition() but the order is
        [position_0, position_1, position_2]

        When the loop is not finished, the order is
        [position_0, position_1, unknown, position_2]

        position_0, position_1, position_2 is the first seen, second seen,
        and third seen key values respectively.
        """

        NUMBER_KEY_VALUES = 3

        if (len(L) == 0):
            return L

        value_positions = {}
        position = 0

        position_0_end = 0 # = position_1_start
        unknown_start = 0 # = position_1_end
        position_2_end = len(L) - 1 # = unknown_last

        while(unknown_start <= position_2_end):
            value = L[unknown_start].value

            if (value not in value_positions):
                if (position < NUMBER_KEY_VALUES):
                    value_positions[value] = position
                    position += 1
                else:
                    error_message = \
                      "L has more than {} key values.".format(NUMBER_KEY_VALUES)
                    raise TypeError(error_message)

            if (value_positions[value] == 0):
                L[unknown_start], L[position_0_end] = \
                L[position_0_end], L[unknown_start]

                unknown_start += 1
                position_0_end += 1
            elif (value_positions[value] == 1):
                unknown_start += 1
            else: # value_positions[value] == 2
                L[unknown_start], L[position_2_end] = \
                L[position_2_end], L[unknown_start]

                position_2_end -= 1

class P1_2_FourKeyPartitioning:
    """
    Keys take one of four values. Reorder L so that all objects of the
    same key appear in the same subarray. The order of the subarrays is
    not important. Use O(1) space and O(|L|) time complexity.
    """

    @staticmethod
    def four_key_partition(L):
        """
        Reorder L so that all objects of the same key appear in the same
        subarray. The order of the subarrays is the order that the key
        values are seen. Use O(1) space and O(|L|) time complexity.
        Keys take one of four values.

        This works the same as three_way_partition() but the order is
        [position_0, position_1, position_2, position_3]
        position_[0-2] work the same as in three_way_partition().
        position_3 is similar to position_2. When a key is to be put in
        the position_3 partition, we rotate the elements in the
        position_2 partition to open up a spot for the position_3 key.
        We swap in the position_3 element and decrement position_2_end
        and position_3_end because they both moved down an index.

        Example:
        [0, 0, 1, 1, 3, X, X, 2, 2, 3, 3]
               ^     ^     ^     ^
               |     |     |     |position_3_end == position_2_start
               |     |     |
               |     |     |position_2_end == unknown_last
               |     |
               |     |unknown_start == position_1_end
               |
               |position_0_end == position_1_start

        The numbers in the figure above stand for the position the
        keys belong to. The X are unknown keys. The 3 at unknown_start
        is the current unknown that is about to be swapped.

        First we rotate the 2 partition by swapping position_3_end
        and position_2_end.
        [0, 0, 1, 1, 3, X, 2, 2, X, 3, 3]

        Then we move the 3 into the 3 partition by swapping unknown_start
        and position_3_end.
        [0, 0, 1, 1, X, X, 2, 2, 3, 3, 3]

        Now we decrement position_3_end and position_2 end. unknown_start
        points at a new unknown for the next iteration so we keep it the same.
        [0, 0, 1, 1, X, X, 2, 2, 3, 3, 3]
               ^     ^  ^     ^
               |     |  |     |position_3_end == position_2_start
               |     |  |
               |     |  |position_2_end == unknown_last
               |     |
               |     |unknown_start == position_1_end
               |
               |position_0_end == position_1_start

        When the loop is not finished, the order is
        [position_0, position_1, unknown, position_2, position_3]

        position_0, position_1, position_2, position_3 is the
        first seen, second seen, third seen, and fourth seen
        key values respectively.
        """

        NUMBER_KEY_VALUES = 4

        if (len(L) == 0):
            return L

        value_positions = {}
        position = 0

        position_0_end = 0 # = position_1_start
        unknown_start = 0 # = position_1_end
        position_2_end = len(L) - 1 # = unknown_last
        position_3_end = len(L) - 1 # = position_2_start

        while(unknown_start <= position_2_end):
            value = L[unknown_start].value

            if (value not in value_positions):
                if (position < NUMBER_KEY_VALUES):
                    value_positions[value] = position
                    position += 1
                else:
                    error_message = \
                      "L has more than {} key values.".format(NUMBER_KEY_VALUES)
                    raise TypeError(error_message)

            if (value_positions[value] == 0):
                L[unknown_start], L[position_0_end] = \
                L[position_0_end], L[unknown_start]

                unknown_start += 1
                position_0_end += 1
            elif (value_positions[value] == 1):
                unknown_start += 1
            elif (value_positions[value] == 2):
                L[unknown_start], L[position_2_end] = \
                L[position_2_end], L[unknown_start]

                position_2_end -= 1
            else: # value_positions[value] == 3
                L[position_3_end], L[position_2_end] = \
                L[position_2_end], L[position_3_end]

                L[unknown_start], L[position_3_end] = \
                L[position_3_end], L[unknown_start]

                position_2_end -= 1
                position_3_end -= 1
