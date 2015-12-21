def extend_to_length(L, element, length):
    """
    Extends L to length with copies of element if length > len(L).
    """

    if (length > len(L)):
        L.extend([element] * (length - len(L)))

def counting_sort(L):
    """
    Return a sorted list such that all objects in L of the same key appear
    in the same subarray.  The order of the subarrays is from keys with
    the lowest to highest value. Keys can take on any number of values.
    The number of values will be figured out.

    This works by first counting the number of keys that take on a value.
    The counts list will be extended as we discover keys with higher
    value.

    Next, the starting indices of each value will be computed in the
    value_starts list.

    Finally, the list is sorted into a new list by putting each key in their
    starting indices by their value. The starting index is incremented each
    time a key is put in place.

    Uses O(n + k) space and O(n + k) time where k is the number of values
    for keys. The largest key value determines k because the list will
    be extended to this value.

    If key value space is large and sparse, we can make counts a dictionary
    instead. This would require sorting the dictionary by key after doing
    the count (first loop). This would take j*log(j) time to sort, where
    j is the number of values for keys that appear at least once in L.
    j is a subset of k.
    After sorting, the second loop would take j time because only the
    elements that exist in the dictionary are looped over.
    Using a list takes k time in the second loop because values with a count
    of 0 are also looped over. The benefit is that a list doesn't require
    a sort.

    So in summary, a dict uses j*log(j) + j time to sort and do the second
    loop. A list uses k time to do the second loop.

    Since j is a subset of k, if k is large and not many values of k is used
    in L (sparse), then j*log(j) + j < k. But if j is close to k,
    j*log(j) + j > k.
    """

    counts = []
    for key in L:
        value = key.value

        required_length = value + 1
        extend_to_length(counts, 0, required_length)

        counts[value] += 1

    value_start_accumulator = 0
    value_starts = [None] * len(counts)
    for i, count in enumerate(counts):
        value_starts[i] = value_start_accumulator
        value_start_accumulator += count

    sorted_L = [None] * len(L)
    for key in L:
        value = key.value

        sorted_L[value_starts[value]] = key
        value_starts[value] += 1

    return sorted_L
