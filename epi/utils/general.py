class key:
    """
    A key that holds a value.
    """

    def __init__(self, value):
        """
        Create a key with a value.
        """

        self.value = value

    def __repr__(self):
        """
        Return the representation of self. Looks like key(value=1).
        """

        return "{}(value={!r})".format(self.__class__.__name__, self.value)
