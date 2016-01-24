class P1_MaxDiff:
    """
    Compute the max difference in a list, L.
    """

    @staticmethod
    def brute_force(L):
        """
        Return max difference by using brute force.

        Checks all possible differences and finds the max.
        """

        max_diff = -float("inf")
        length = len(L)
        for i in range(length - 1):
            start = L[i]
            for j in range(i + 1, length):
                end = L[j]
                diff = end - start
                max_diff = max(max_diff, diff)
        return max_diff

    @classmethod
    def divide_and_conquer(cls, L):
        """
        Return max difference by using divide and conquer.

        Splits list in 2. Max difference is the max difference of the left
        the right, and the between. The between is the max of the right minus
        the max of the left.
        """

        length = len(L)
        if (length <= 1):
            return -float("inf")
        left_L = L[0 : length//2]
        right_L = L[length//2 :]
        left_max_diff = cls.divide_and_conquer(left_L)
        right_max_diff = cls.divide_and_conquer(right_L)
        middle_max_diff = max(right_L) - min(left_L)
        return max(left_max_diff, right_max_diff, middle_max_diff)

    @staticmethod
    def previous_min(L):
        """
        Return max difference by keeping track of the previous minimum.

        Uses the previous minimum to calculate a new difference and update
        the current max difference if it is bigger.
        """

        mini = float("inf")
        max_diff = -float("inf")
        for e in L:
            # find max_diff using PREVIOUS minimum
            max_diff = max(max_diff, e - mini)
            # after finding current max_diff, can update the previous minimum
            mini = min(mini, e)
        return max_diff
