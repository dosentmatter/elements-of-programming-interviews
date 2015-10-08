def range_length(*args):
    """
    Returns the number of iterations of a Python range() mathematically.
    The parameters are the same as the Python range() - either
    (stop) or (start, stop[, step]).

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
    if (length == 1):
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
