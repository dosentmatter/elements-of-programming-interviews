def range_length(*args):
    """
    Return the number of iterations of a Python range() mathematically.
    The parameters are the same as the Python range() - either
    (stop) or (start, stop[, step]). You can actually just use
    len(range(stop)) or len(range(start, stop[, step])). This function
    turns out to be useless.

    The calculation works as follows:
    It is easier to show a concrete example so I will choose values for
    start, stop, and step.
    Assuming there are elements and step is positive.
    start == 0
    stop == 12
    step == 3

    Here is the range of items:
    0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11
    |        |        |        |
    There are (stop - step) == 11 elements = number_elements.
    The bars mark the elements that will be returned by the range.
    The length is 4, now we have to find a way to calculate this.

    First remove the 0:
       1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11
       ------| -------| -------| -------
    The number of elements now == number_elements_no_zero.
    Each of the bars with dashes are called groups. Each of these groups
    have step elements. The last set of dashes (10, 11) is not a group
    because it does not have step elements. This means that we can
    calculate the number of groups by calculating
    number_elements_no_zero // step == 3 == number_step_groups

    Now we add back in the zero:
    groups_including_zero == number_step_groups + 1 == 4 == length

    This can be extended to any other example with a positive step, and
    number_elements > 0. Where start and step is doesn't matter. For
    example, you could have added 10 to start and step in my example above.
    0 would be representative of the first element, and 11 of the last.

    If step < 0, we can just negate start, stop, and step. For a range(),
    this would just produce the negated elements so length stays the same:
    list(range(5, -10, -3)) == [5, 2, -1, -4, -7]
    list(range(-5, 10, 3)) == [-5, -2, 1, 4, 7]
    """

    length = len(args)
    start = 0
    step = 1
    if (length == 0):
        raise TypeError("range_length expected 1 argument, got 0")
    elif (length == 1):
        stop = args[0]
    elif (length == 2):
        start, stop = args
    elif (length == 3):
        start, stop, step = args
    else:
        error_message = \
            "range_length expected at most 3 arguments, got {}".format(length)
        raise TypeError(error_message)

    if (step == 0):
        raise TypeError("range() arg 3 must not be zero")
    elif (step < 0):
        start, stop, step = -start, -stop, -step

    number_elements = stop - start
    if (number_elements <= 0):
        return 0
    number_elements_no_zero = number_elements - 1
    number_step_groups = number_elements_no_zero // step
    groups_including_zero = number_step_groups + 1
    return groups_including_zero

def max_diff(iterable):
    """
    Return max difference by keeping track of the previous minimum.
    iterable must have >= 2 elements.

    Uses the previous minimum to calculate a new difference and update
    the current max difference if it is bigger.
    """

    iterable = iter(iterable)
    try:
        e0 = next(iterable)
        e1 = next(iterable)
    except StopIteration:
        raise ValueError("iterable must have >= 2 elements.")
    mini = min(e0, e1)
    max_diff = e1 - e0
    for e in iterable:
        # find max_diff using PREVIOUS minimum
        max_diff = max(max_diff, e - mini)
        # after finding current max_diff, can update the previous minimum
        mini = min(mini, e)
    return max_diff

def max_diff_reversed(iterable):
    """
    Return the reversed max difference by keeping track of the previous
    maximum. iterable must have >= 2 elements.
    The reversed max difference equivalent to max_diff(reversed(iterable)),
    but this does not require reversing the iterable, which might require
    extra space to reverse if it is not a sequence.
    max_diff_reversed(reversed(iterable)) is equivalent to
    max_diff(iterable) but max_diff_reversed just works backwards.

    Uses the previous maximum to calculate a new difference and update
    the current max difference if it is bigger.
    """

    iterable = iter(iterable)
    try:
        e0 = next(iterable)
        e1 = next(iterable)
    except StopIteration:
        raise ValueError("iterable must have >= 2 elements.")
    maxi = max(e0, e1)
    max_diff = e0 - e1
    for e in iterable:
        # find max_diff using PREVIOUS maximum
        max_diff = max(max_diff, maxi - e)
        # after finding current max_diff, can update the previous maximum
        maxi = max(maxi, e)
    return max_diff

def max_diff_generator(iterable):
    """
    Generate the max difference so far by keeping track of the previous minimum.
    iterable must have >= 2 elements.

    Uses the previous minimum to calculate a new difference and update
    the current max difference if it is bigger.

    Note that the generator will have 1 element less than the iterable because
    there are k-1 possible differences in a iterable of size k.
    """

    iterable = iter(iterable)
    try:
        e0 = next(iterable)
        e1 = next(iterable)
    except StopIteration:
        raise ValueError("iterable must have >= 2 elements.")
    mini = min(e0, e1)
    max_diff = e1 - e0
    yield max_diff
    for e in iterable:
        # find max_diff using PREVIOUS minimum
        max_diff = max(max_diff, e - mini)
        yield max_diff
        # after finding current max_diff, can update the previous minimum
        mini = min(mini, e)

def max_diff_reversed_generator(iterable):
    """
    Generate the reversed max difference so far by keeping track of the
    previous maximum. iterable must have >= 2 elements.

    Uses the previous maximum to calculate a new difference and update
    the current max difference if it is bigger.

    Note that the generator will have 1 element less than the iterable because
    there are k-1 possible differences in a iterable of size k.
    """

    iterable = iter(iterable)
    try:
        e0 = next(iterable)
        e1 = next(iterable)
    except StopIteration:
        raise ValueError("iterable must have >= 2 elements.")
    maxi = max(e0, e1)
    max_diff = e0 - e1
    yield max_diff
    for e in iterable:
        # find max_diff using PREVIOUS maximum
        max_diff = max(max_diff, maxi - e)
        yield max_diff
        # after finding current max_diff, can update the previous maximum
        maxi = max(maxi, e)

def enumerate_step(iterable, start=0, step=1):
    """
    Return an iterator that enumerates iterable with step from start.
    Works the same as Python's enumerate() but has a step.
    """

    if (step == 1):
        return enumerate(iterable, start)
    else:
        return izip(count(start, step), iterable)
