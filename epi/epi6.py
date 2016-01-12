from epi.utils import listextra, randomextra

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

        This works the same as three_key_partition() but the order is
        [position_0, position_1, position_2, position_3]
        position_[0-2] work the same as in three_key_partition().
        position_3 is similar to position_2 in three_key_partition().
        When a key is to be put in the position_3 partition, we rotate
        the elements in the position_2 partition to open up a spot for
        the position_3 key. We swap in the position_3 element and
        decrement position_2_end and position_3_end because they both
        moved down an index.

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

class P1_3_TwoKeyPartitioning:
    """
    Keys take one of two (or boolean) values. Reorder L so that all
    objects of the same key appear in the same subarray. The order
    of the subarrays is not important.
    Use O(1) space and O(|L|) time complexity.
    """

    @staticmethod
    def two_key_partition(L):
        """
        Reorder L so that all objects of the same key appear in the same
        subarray. The order of the subarrays is the order that the key
        values are seen. Use O(1) space and O(|L|) time complexity.
        Keys take one of two (or boolean) values.

        This works the same as three_key_partition() but the order is
        [position_0, position_1]
        position_0 works the same as position_1 in three_key_partition()
        position_1 works the same as position_2 in three_key_partition()

        position_0 of three_key_partition() wasn't chosen to use as a
        partition because it requires more work compared to the other
        ones. It does a swap and two increments.
        In three_key_partition(),
        position_1 does one increment.
        position_2 does one swap and one decrement.

        When the loop is not finished, the order is
        [position_0, unknown, position_1]

        position_0 and position_1 is the first seen and second seen
        key values respectively.
        """

        NUMBER_KEY_VALUES = 2

        if (len(L) == 0):
            return L

        value_positions = {}
        position = 0

        unknown_start = 0 # = position_0_end
        position_1_end = len(L) - 1 # = unknown_last

        while(unknown_start <= position_1_end):
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
                unknown_start += 1
            else: # value_positions[value] == 1
                L[unknown_start], L[position_1_end] = \
                L[position_1_end], L[unknown_start]

                position_1_end -= 1

class P2_UninitializedArray:
    """
    Design a deterministic scheme by which reads and writes to an
    uninitialized array can be made in O(1) time. You may use O(n)
    additional storage; reads to uninitialized entry should return
    false. The array can hold any data, not just boolean.
    """

    class UninitializedArray:
        """
        An uninitialized array with reads and writes that are O(1).

        This array is backed up by three lists - index_elements,
        index_initialize_times, and initialize_time_indices. It is easier to
        think of these lists as maps rather than lists. index_elements
        maps indices to elements, index_initialize_times maps indices to
        initialize times, and initialize_time_indices maps initialize times
        to indices.

        index_elements is the list that holds the actual data. It may be wrong
        depending if the index was initialized.

        The other two lists are used to check if the data has been initialized.

        initialize time is the time that an element at an index was initialized.
        For example, the first call to __setitem__ would be the 0th
        initialize time. The next call would be the 1st initialize time.

        number_initialized is the amount of elements that have been initialized.
        initialize times < number_initialized have been initialized because
        number_initialized is only incremented when elements are initialized.

        index_initialize_times tells when an index was initialized.
        It may be wrong depending if the index was initialized.

        initialize_time_indices tells which index was initialized at an
        initialize time. All initialize_time < number_initialized are correct.
        Which means the indices that these initialize_time are mapped to
        have been initialized.

        Notice that initialize_time_indices is the only list that tells
        true information up to number_initialized because the elements are
        written sequentially. The other two lists, index_elements and
        index_initialize_times may be true or false because they are written
        randomly and we can't use anything to track random writes such as
        a dictionary.

        So this means one way to read an index is to check all
        initialize_time < number_initialized and see if initialize_time_indices
        contains the index being read. If the index is contained, we return
        the element in index_elements at that index. Otherwise, we return False.
        We can do this because we know that index has been initialized.
        However, this takes O(n) time and we want O(1) time.
        This is why we include index_initialize_times.

        Notice that index_initialize_times is just the opposite mapping
        of initialize_time_indices. index_initialize_times is used to speed
        up the search to see if an index has been initialized. Instead of doing
        an O(n) search through initialize_time_indices when doing a read, we 
        index into index_initialize_times and use the initialize_time
        given see if the index has been written.

        An example will make this easier to explain.
        Let's say we want to read the element at index 6.
        We don't know if index_elements[6] is correct because we don't know
        if it has been initialized. We also, don't know if
        index_initialize_times[6] is correct for the same reason, but we
        can use it to help us.

        Let's say index_initialize_times[6] == 7. This is saying
        the element at index 6 was initialized at time 7 which may or may not
        be true.
        Let the proposition, P be
        P: The element at index 6 was initialized at time 7

        Let's say number_initialized == 20. Since 7 < 20, P may still be
        true. If number_initialized was 4, we know that P is false because
        we haven't initialized up to the 7th initialize time yet. This
        means index_elements[6] and index_initialize_times[6] has
        uninitialized data and we return False.

        So we continue with number_initialized == 20. We use 7 (an initialize
        time) to index into initialize_time_indices. If
        initialize_time_indices[7] == 6, we know index 6 has been initialized
        because initialize_time_indices is true up to number_initialized == 20.
        We can then return index_elements[6] and this all took O(1) time.

        In summary,
        P: initialize_time_indices[7] == 6
        Q: index 6 is initialized
        P => Q is true

        The problem comes when initialize_time_indices[7] != 6. We have to
        prove that this implies that index 6 is uninitialized.
        So let
        P: initialize_time_indices[7] != 6
        Q: index 6 is uninitialized
        Does P => Q?
        Notice this implication is the inverse of the above one.

        I will prove this by contradiction. Assume P => Q is false. This
        means that if P: initialize_time_indices[7] != 6, then
        (not Q): index 6 is initialized. If index 6 is initialized, this
        means that index_initialize_times[6] == 7 is true because index
        6 has been initialized. But initialize_time_indices[7] != 6 is
        also true because 7 < (number_initialized == 20), which contradicts
        with index_initialize_times[6] == 7. Proof by contradiction,
        so P => Q is true.

        You can generalize the example to when a different index is
        being read.
        """

        def __init__(self, length):
            """
            Initialize this array of length length with random data.
            The random data represents the uninitialized data a malloc
            would give.

            Set up the lists with random integers up to a maximum of
            ARBITRARY_MAX_INT that was chosen arbitrarily.
            """

            ARBITRARY_MAX_INT = 1000000

            self.length = length

            self.index_elements = \
                randomextra.randlist_duplicates(ARBITRARY_MAX_INT, length)
            self.index_initialize_times = \
                randomextra.randlist_duplicates(ARBITRARY_MAX_INT, length)
            self.initialize_time_indices = \
                randomextra.randlist_duplicates(ARBITRARY_MAX_INT, length)

            self.number_initialized = 0

        def __setitem__(self, index, value):
            """
            Set the item at index to value.

            Indices are initialized the first time they are written to.
            """

            self.index_elements[index] = value

            if (not self.is_initialized(index)):
                self.initialize(index)

        def __getitem__(self, index):
            """
            Get the item at index.

            Data is only valid if the index is initialized. If invalid,
            return False.
            """

            result = False

            if (self.is_initialized(index)):
                result = self.index_elements[index]

            return result

        def initialize(self, index):
            """
            Initialize index.

            index_initialize_times and initialize_time_indices are opposite
            maps so they both get the information that index is the next
            index being initialized. The current initialization time is
            number_initialized. After this time is used, we increment it.
            """

            self.index_initialize_times[index] = self.number_initialized
            self.initialize_time_indices[self.number_initialized] = index

            self.number_initialized += 1

        def is_initialized(self, index):
            """
            Return True if index is initialized.

            This is explained in the class docstring where indices are only
            valid after they have been initialized.
            """

            initialize_time = self.index_initialize_times[index]
            return (initialize_time < self.number_initialized) and \
                   (self.initialize_time_indices[initialize_time] == index)

        def __len__(self):
            """
            Return the length of this array.
            """

            return self.length
