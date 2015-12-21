import random

def randlist_duplicates(max_number, length, min_number=0):
    """
    Return a list of length length with elements ranging from
    [min_number, max_number]. There can be duplicates.
    """

    return \
    [random.randint(min_number, max_number) for _ in range(length)]

def randlist_from_list(L, length):
    """
    Return a list of length length with elements from L.
    There can be duplicates. If no duplicates are wanted, just
    use random.sample.
    """

    return \
    [random.choice(L) for _ in range(length)]

def randlist_subset(max_number, length, subset_length, min_number=0):
    """
    Return a list of length length with elements from a subset
    (of length subset_length) of the range [min_number, max_number].
    There can be duplicates. If no duplicates are wanted, just
    use random.sample.

    For example, if subset_length == 3, 3 distinct elements would
    be sampled from the range [min_number, max_number] and a random
    list would be generated from these 3 elements, with duplicates.
    """

    subset = randlist_no_duplicates(max_number, subset_length, min_number)
    return randlist_from_list(subset, length)

def randlist_boolean(length):
    """
    Return a list of length length with boolean elements. There can be
    duplicates.
    """

    return randlist_from_list([True, False], length)

def randlist_no_duplicates(max_number, length, min_number=0):
    """
    Return a list of length length with elements ranging from
    [min_number, max_number]. There are no duplicates.
    """

    return random.sample(range(min_number, max_number + 1), length)
