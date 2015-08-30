def get_bit(x, k):
    """
    Return the k-th bit of x.
    """
    return (x >> k) & 1

def toggle_bit(x, k):
    """
    Return x with the k-th bit toggled.
    """
    return (1 << k) ^ x

def drop_LSB(x):
    """
    Return x with the LSB (least significant bit) set to 0.
    """
    return x & (x - 1)

def swap_bits(x, i, j):
    """
    Swap bits by toggling bits i and j of x if different.
    """
    if (get_bit(x, i) != get_bit(x, j)):
        x = toggle_bit(toggle_bit(x, i), j)
    return x