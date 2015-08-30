class MaxDiff:
    """
    Compute the max difference in an array, S.
    """

    @staticmethod
    def brute_force(S):
        """
        Return max difference by checking all differences.
        """
        max_diff = -float("inf")
        length = len(S)
        for i in range(length - 1):
            start = S[i]
            for j in range(i + 1, length):
                end = S[j]
                diff = end - start
                max_diff = max(max_diff, diff)
        return max_diff

    @classmethod
    def divide_and_conquer(cls, S):
        """
        Return max difference by splitting list in 2. Max difference is the max difference
        of the left, the right, and the between. The between is the max of the right minus
        the max of the left.
        """
        length = len(S)
        if (length == 1):
            return -float("inf")
        L = S[0 : length//2]
        R = S[length//2 :]
        l = cls.divide_and_conquer(L)
        r = cls.divide_and_conquer(R)
        m = max(R) - min(L)
        return max(l, r, m)

    @staticmethod
    def previous_min(S):
        """
        Return max difference by keeping track of the previous minimum and the current max difference.
        """
        mini = float("inf")
        max_diff = -float("inf")
        for i in range(len(S)):
            max_diff = max(max_diff, S[i] - mini) # find max_diff using PREVIOUS minimum
            mini = min(mini, S[i]) # after finding current max_diff, can update the previous minimum
        return max_diff
