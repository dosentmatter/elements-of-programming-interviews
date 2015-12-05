from epi.util import python
import itertools, functools, operator

def ones(n, offset=0):
    """
    Return a number that is a stream of n 1's with an offset. If
    n is infinite, return -1
    """

    if (n == float('inf')):
        return -1

    return ((1 << n) - 1) << offset

def get_bit(x, k):
    """
    Return the k-th bit of x.
    """

    return (x >> k) & 1

def get_bit_position(x, k):
    """
    Return the k-th bit of x, leaving it in its position.
    """

    return x & (1 << k)

def set_bit(x, k):
    """
    Return x with the k-th bit set.
    """

    return x | (1 << k)

def unset_bit(x, k):
    """
    Return x with the k-th bit unset.
    """

    return x & ~(1 << k)

def toggle_bit(x, k):
    """
    Return x with the k-th bit toggled.
    """

    return x ^ (1 << k)

def drop_lowest_set_bit(x):
    """
    Return x with the lowest set bit set to 0.
    """

    return x & (x - 1)

def drop_lowest_unset_bit(x):
    """
    Return x with the lowest unset bit set to 1.
    """

    return x | (x + 1)

def right_extend_lowest_set_bit(x):
    """
    Return x with the lowest set bit extended to the right.

    Example:
    0b 1010 0000 -> 1011 1111
    """

    return x | (x - 1)

def right_extend_lowest_unset_bit(x):
    """
    Return x with the lowest unset bit extended to the right.

    Example:
    0b 0101 1111 -> 0100 0000
    """

    return x & (x + 1)

def get_lowest_set_bit(x):
    """
    Return a number with only the lowest set bit of x set high.

    Example:
    0b 0010 0100 -> 0b 0000 0100

    Notice -x == ~x + 1 == ~(x - 1) from two's complement.

    Proof for ~x + 1 == ~(x - 1):
    ~x + 1 == -x
    ~x == -x - 1 == -(x + 1)
    ~(x - 1) == -((x - 1) + 1) == -x
    """

    return x & -x

def get_lowest_unset_bit(x):
    """
    Return a number with only the lowest unset bit of x set high.

    Example:
    0b 1010 1011 -> 0b 0000 0100
    """

    return ~x & (x + 1)

def is_set(x, k):
    """
    Return True if the kth bit of x is set.
    """

    return get_bit(x, k) == 1

def is_even(x):
    """
    Return True if x is even.
    """

    return (x & 1) == 0

def is_odd(x):
    """
    Return True if x is odd.
    """

    return (x & 1) == 1

def is_power_two(x):
    """
    Return True if x is a power of two - meaning x only has one bit set
    high.
    """

    return (x != 0) and (drop_lowest_set_bit(x) == 0)

def get_least_significant_bits(x, n):
    """
    Return the n least significant bits of x.
    """

    return x & ones(n)

def get_bits(x, k, size, offset=0):
    """
    Return the k-th set of size bits starting from offset.
    """

    answer = x >> offset
    answer >>= k * size
    return get_least_significant_bits(answer, size)

def split_bits_index(x, k):
    """
    Return two numbers - one with the lower bits of x (x[0:k]) and one with
    the upper bits of x (x[k:]). Notice k == 0, float('inf') to give upper
    or lower all the bits respectively.
    """

    mask = ones(k)

    lower = x & mask
    upper = x & ~mask

    return lower, upper

def split_bits_bit_array(x, bit_array):
    """
    bit_array has one bit set high. Let k == log2(bit_array).
    Return two numbers - one with the lower bits of x (x[0:k]) and one with
    the upper bits of x (x[k:]). This means that the bits below the 1 in
    bit_array belong to lower and the rest belong to upper. Notice k == 1, 0
    to give upper or lower all the bits respectively.

    You can think of k == 0 gives lower all the bits because
    log2(0) == float('inf') if you think of log2 meaning how many right shifts
    until the number equals 1. For 0, there will be infinite right shifts,
    because the 1 is infinitely high up. If you follow the real meaning of log2,
    log2(0) == -float('inf') so it won't make as much sense.
    """

    mask = bit_array - 1

    lower = x & mask
    upper = x & ~mask

    return lower, upper

def swap_bits_index(x, i, j=python.Parameter.OTHER_ARGUMENT):
    """
    Return x with bits swapped by toggling bits i and j of x if different.
    j defaults to i + 1.
    """

    if (j is python.Parameter.OTHER_ARGUMENT):
        j = i + 1

    if (get_bit(x, i) != get_bit(x, j)):
        x = toggle_bit(toggle_bit(x, i), j)
    return x

def swap_bits_bit_array(x, bit_array):
    """
    Return x with bits swapped according to bit_array. If bit_array has
    two bits set high, these two bits indicate the two bits that you
    want to swap. If bit_array only has one bit set high, the second bit
    defaults to the first bit index + 1. If bit_array has no bits set high,
    nothing is swapped.

    Example:
    This swaps the 0th and the 3rd bits.
    bit_array == 0b 01001

    This works by checking if the bits being swapped differ. If they differ,
    they are both toggled.

    To check if the bits differ, we check if the masked x, x & bit_array
    is a power of two.

    x & bit_array can be 3 types of numbers shown in regex:
    0b 0* 1 0* 1 0* - two 1's, happens when both bits in x are 1's
    0b 0*           - all 0's, happens when both bits in x are 0's
    0b 0* 1 0*      - one 1, happens when both bits in x differ

    So you see, when the masked x has a single one (a power of two), the
    bits being swapped in x differ.

    To toggle the bits, we just xor by bit_array
    """

    if (is_power_two(bit_array)):
        bit_array |= bit_array << 1

    if (is_power_two(x & bit_array)):
        x ^= bit_array
    return x

def shift_bits(x, k):
    """
    Return x logically right shifted by k. k can be negative, which would
    mean a logical left shift.
    """
    if (k >= 0):
        return x << k
    else:
        return x >> -k

def shift_trailing_zeros(x):
    """
    Return x with the trailing 0's shifted out (to the right). You can
    also think of it as shifting the lowest set bit to the 0th bit. If
    there are no 1's return 0.
    """

    if (x == 0):
        return 0

    return x // get_lowest_set_bit(x)

def shift_trailing_ones(x):
    """
    Return x with the trailing 1's shifted out (to the right). You can
    also think of it as shifting the lowest unset bit to the 0th bit. If
    there are no 0's, return -1.
    """

    if (x == -1):
        return -1

    return x // get_lowest_unset_bit(x)

def shift_lowest_set_bit_index(x, k):
    """
    Return x with the lowest set bit shifted to the k-th bit.
    If there are no 1's, return 0.

    This can use shift_trailing_zeros() on x first because the lost 0's will
    be shifted back in.
    """

    return shift_trailing_zeros(x) << k

def shift_lowest_unset_bit_index(x, k):
    """
    Return x with the lowest unset bit shifted to the k-th bit.
    If there are no 0's, return -1.

    This can't use shift_trailing_ones() on x first because the
    ones will be lost.
    """

    if (x == -1):
        return -1

    return (x << k) // get_lowest_unset_bit(x)

def shift_lowest_set_bit_bit_array(x, bit_array):
    """
    Return x with the lowest set bit shifted to the k-th bit. bit_array
    has only the k-th bit set high indicating the bit to shift to. If there
    are no 1's. return 0.

    This can use shift_trailing_zeros() on x first because the lost 0's will
    be shifted back in.
    """

    return shift_trailing_zeros(x) * bit_array

def shift_lowest_unset_bit_bit_array(x, bit_array):
    """
    Return x with the lowest unset bit shifted to the k-th bit. bit_array
    has only the k-th bit set high indicating the bit to shift to. If there
    are no 0's, return -1.

    This can't use shift_trailing_ones() on x first because the
    ones will be lost.
    """

    if (x == -1):
        return -1

    return (x * bit_array) // get_lowest_unset_bit(x)

def get_consecutive_diff(x):
    """
    Find sequences of two consecutive bits that differ starting
    from the least significant bit and return a number with the
    less significant bits set high.

    Example:
    0b 10 1011 1000 -> 0b 11 1110 0100
    """

    return x ^ (x >> 1)

def get_consecutive_01(x):
    """
    Find sequences of bits, 01, in x starting from the least
    significant bit and return a number with the 1 bits set high.

    Example:
    0b 10 1011 1000 -> 0b 10 1010 0000

    This masks get_consecutive_diff() with x because x has a 1 bit
    in the 1 position in 01.
    """

    return get_consecutive_diff(x) & x

def get_consecutive_10(x):
    """
    Find sequences of bits, 10, in x starting from the least
    significant bit and return a number with the 0 bits set high.

    Example:
    0b 10 1011 1000 -> 0b 01 0100 0100

    This masks get_consecutive_diff() with (x >> 1) because (x >> 1)
    has a 1 bit in the 0 position in 10.
    """

    return get_consecutive_diff(x) & (x >> 1)

def get_first(x, get_bit_array_indices):
    """
    Returns a number with the first index bit set high. For example,
    if get_bit_array_indices == get_consecutive01(), this function
    would return a number with the 1 set high in the first 01.
    """

    bit_array = get_bit_array_indices(x)
    return get_lowest_set_bit(bit_array)

def same_bits_up(x):
    """
    Return the closest number greater than x that has the same number of
    bits set high as x.

    Example:
    9 == 0b 1001 -> 10 == 0b 1010
    10 == 0b 1010 -> 12 == 0b 1100
    12 == 0b 1100 -> 17 == 0b 1 0001

    From the example, you can see that this works by swapping the first
    consecutive 01 then shifting the 1's before the consecutive 01 all
    the way down.

    Here are the cases you will see:
    0b 01 111000 -> 0b 10 000111
    0b 01 111111 -> 0b 10 111111
    0b 01 000000 -> 0b 10 000000
    0b 00 000000 -> 0b 00 000000
    0b ...111000 -> 0b ...111000
    0b ...111111 -> 0b ...111111

    negative numbers:
    -13: 0b ...10011 -> -11
    -11: 0b ...10101 -> -10
    -10: 0b ...10110 -> -7
    -7 : 0b ...11001 -> -6
    -6 : 0b ...11010 -> -4
    -4 : 0b ...11100 -> -4
    """

    bit_array = get_first(x, get_consecutive_01)

    if (bit_array == 0):
        return x

    lower, upper = split_bits_bit_array(x, bit_array)
    upper = swap_bits_bit_array(upper, bit_array)
    lower = shift_trailing_zeros(lower)

    return upper | lower

def same_bits_down(x):
    """
    Return the closest number less than x that has the same number of
    bits set high as x.

    Example:
    12 == 0b 1100 -> 10 == 0b 1010
    10 == 0b 1010 -> 9 == 0b 1001
    9 == 0b 1001 -> 6 = 0b 0110

    From the example, you can see that this works by swapping the first
    consecutive 10 then shifting the 1's before the consecutive 10 all
    the way up (to the bit position right before the 10). In the code,
    the shifting the 1's part is done by shifting the first unset bit
    to the 0 position in the 10. This is less complex and does the same
    thing because there will be a stream of 1's. This is explained
    more clearly below

    Here are the cases you will see:
    0b 10 000111 -> 0b 01 111000
    0b 10 000000 -> 0b 01 000000
    0b 10 111111 -> 0b 01 111111
    0b ...111111 -> 0b ...111111
    0b 00 000111 -> 0b 00 000111
    0b 00 000000 -> 0b 00 000000

    In the 1st and 3rd cases, you see in the lower part of the number, there
    are a stream of 1's if there are to be any 1's. There can't be a 0 between
    the 1's, otherwise the 10 would have appeared earlier. For the lower part,
    we want to shift up the 1's to the bit position before the 0 in the 10.
    You can do this by finding the highest 1 in the lower part (most significant
    bit in the lower part) and shifting it up. Or by shifing the lowest 0 bit
    to the bit position of the 0 in 10 since you know there will be a stream of
    1's. Shifting a 0 is less complex so that is done in the code.

    negative numbers:
    -1 : 0b ...11111 -> -1
    -4 : 0b ...11100 -> -6
    -6 : 0b ...11010 -> -7
    -7 : 0b ...11001 -> -10
    -10: 0b ...10110 -> -11
    -11: 0b ...10101 -> -13
    -13: 0b ...10011 -> -18
    """

    bit_array = get_first(x, get_consecutive_10)

    if (bit_array == 0):
        return x

    lower, upper = split_bits_bit_array(x, bit_array)
    upper = swap_bits_bit_array(upper, bit_array)
    lower = shift_lowest_unset_bit_bit_array(lower, bit_array)

    return upper | lower

def log2(x):
    """
    Return the log base 2 of x.

    Finds the highest amount x can be rightshifted by a multiple of 2.
    Then goes downwards looking for any amounts x can still be rightshifted.
    If x has multiple 1-bits, the most significant one will be used.
    
    Example:
    x == 1 << 59
    59 == 0b11 1011    # binary

    The highest amount x can be rightshifted by a multiple of 2 is 32.
    x >> = 32
    x == 1 << 27
    27 == 0b01 1011

    Now, the highest x can be rightshifted by is 16 == 32 >> 1.
    x >> 16
    x == 1 << 11
    11 == 0b00 1011

    Keep going, and x can still be shifted by 8, 2, and 1. At this point,
    x == 1 << 0 == 1.

    The answer will be the sum of the shifts: 32 + 16 + 8 + 2 + 1 == 59.
    """

    if (x == 0):
        return -float("inf")
    elif (x == 1):
        return 0

    highest_shift_amount = 1
    while (True):
        if (x >> highest_shift_amount):
            highest_shift_amount <<= 1
        else:
            highest_shift_amount >>= 1    # backtrack
            break

    shift_amount = highest_shift_amount

    answer = 0
    while (x != 1):
        if (x >> shift_amount):
            x >>= shift_amount
            answer += shift_amount
        shift_amount >>= 1
    return answer

def log2_cached_creator():
    """
    Return a closure that caches log2 answers.
    """

    log2_dict = {}
    log2_dict[0] = -float("inf")
    max_shift_amount = 0

    def closure(x):
        """
        Given an x, This will find and cache all solutions of numbers less
        than x if they haven't already been cached. Only works for x that
        is a power of 2 (single 1 bit).
        """

        nonlocal max_shift_amount

        if (x in log2_dict):
            return log2_dict[x]

        while (True):
            max_num = 1 << max_shift_amount
            log2_dict[max_num] = max_shift_amount
            max_shift_amount += 1
            if (x == max_num):
                return log2_dict[x]
    return closure

def log2_python(x):
    """
    Return the log base 2 of x using Python's bit_length() method.
    """

    if (x == 0):
        return -float("inf")

    return x.bit_length() - 1

def bit_array_select(L, bit_array, log2):
    """
    Return a frozenset that contains L[k] iff get_bit(bit_array, k) == 1.
    log2 is a function that returns the log2 of a number.
    """

    S = set()
    while (bit_array):
        i = log2(get_lowest_set_bit(bit_array))
        bit_array = drop_lowest_set_bit(bit_array)
        S.add(L[i])
    return frozenset(S)

def majority_bitwise(*bit_arrays):
    """
    Return the bitwise majority of bit_arrays.
    """

    if (len(bit_arrays) == 0):
        raise TypeError("len(bit_arrays) must be > 0.")

    MINIMUM_MAJORITY = (len(bit_arrays) // 2) + 1

    answer = 0
    for bit_array_subset in \
            itertools.combinations(bit_arrays, MINIMUM_MAJORITY):
        answer |= functools.reduce(operator.and_, bit_array_subset)

    return answer

def majority_logical(*bit_arrays):
    """
    Return the logical majority of bit_arrays. Can be used on
    booleans or integers with 1 or 0 bits set. Gives the same
    answer as majority_bitwise() but with short circuiting
    if the integers with 1 bit set have it set at the same
    index.
    """

    if (len(bit_arrays) == 0):
        raise TypeError("len(bit_arrays) must be > 0.")

    MINIMUM_MAJORITY = (len(bit_arrays) // 2) + 1

    answer = itertools.combinations(bit_arrays, MINIMUM_MAJORITY)
    answer = map(all, answer)
    answer = any(answer)
    return answer

def add_bitwise(x, y):
    """
    Return the sum of x and y (unsigned) using only assignment,
    bitwise operators, loops, and conditionals.
    """

    answer = 0
    carry_in = 0
    k = 1
    iterations_tracker = x | y

    while (iterations_tracker):
        x_k = x & k
        y_k = y & k

        answer |= x_k ^ y_k ^ carry_in
        carry_out = majority_bitwise(x_k, y_k, carry_in)

        carry_in = carry_out << 1

        k <<= 1
        iterations_tracker >>= 1

    if (carry_in):
        answer |= carry_in

    return answer

def multiply_bitwise(x, y):
    """
    Return the product of x and y (unsigned) using only assignment,
    bitwise operators, loops, and conditionals.
    """

    answer = 0
    k = 1
    shifted_x = x

    iterations_tracker = y

    while (iterations_tracker):
        if (y & k):
            answer = add_bitwise(answer, shifted_x)

        k <<= 1
        shifted_x <<= 1
        iterations_tracker >>= 1

    return answer
