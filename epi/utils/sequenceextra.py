def sequence_islice(sequence, *args):
    """
    Return an iterator that returns selected elements from the sequence.
    The parameters are the same as the Python itertools.islice() - either
    (sequence, stop) or (sequence, start, stop[, step]). If start, stop,
    or step are None, they default to end values or a single step.
    You can actually just use Python slice notation sequence[::] or
    itertools.islice(). slice notation is the fastest and itertools.islice()
    is the second fastest. sequence_islice is the slowest. This is probably
    because the Python slice notation and itertools.islice is written in C.
    This function turns out to be useless.
    """

    length = len(args)
    start = None
    step = None
    if (length == 0):
        raise TypeError("sequence_islice expected at least 2 arguments, got 1")
    elif (length == 1):
        stop = args[0]
    elif (length == 2):
        start, stop = args
    elif (length == 3):
        start, stop, step = args
    else:
        error_message = \
            "sequence_islice expected at most 4 arguments, got {}"
        error_message = error_message.format(length)
        raise TypeError(error_message)

    if (step is None):
        step = 1

    if (step == 0):
        raise TypeError("sequence_islice() arg 4 must not be zero")
    elif (step > 0):
        if (start is None):
            start = 0
        if (stop is None):
            stop = len(sequence)

        if (start < 0):
            start = 0
        if (stop > len(sequence)):
            stop = len(sequence)
    elif (step < 0):
        reverse_end = (-1 - len(sequence))
        if (start is None):
            start = -1
        if (stop is None):
            stop = reverse_end

        if (start > -1):
            start = -1
        if (stop < reverse_end):
            stop = reverse_end

    return (sequence[i] for i in range(start, stop, step))
