import fractions

def n_choose_r(n, r):
    """
    Return the number of combinations of n choose r.

    Uses a for loop because factorials get big really quickly.
    """

    if ((n < 0) or (r < 0) or (r > n)):
        return 0

    answer = 1
    for i in range(r):
        answer *= fractions.Fraction(n - i, i + 1)
    return int(answer)
