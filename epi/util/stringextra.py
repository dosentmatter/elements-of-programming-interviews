def int_to_digit(x):
    """
    Returns the digit version of the integer x. The digit is represented
    as a length-1 string (a character).

    Supports up to base16 (hexadecimal) digits.  Alphabetical digits
    are lowercase.  If out of range, returns None.
    """

    if (x < 0):
        return None
    elif (x < 10): # 0 to 9
        return chr(ord('0') + x)
    elif (x < 16): # a to f
        return chr(ord('a') + (x - 10))
    else:
        return None

def digit_to_int(c):
    """
    Returns the integer version of the digit c. c is represented as a length-1
    string (a character).

    Supports up to base16 (hexadecimal) digits. Accepts uppercase and lowercase
    alphabetical digits. Returns None if not in the range or digits.
    """

    if (c.isdigit()):
        return ord(c) - ord('0')
    elif (c.isalpha()):
        offset_char = 'a'
        if (c.isupper()):
            offset_char = 'A'
        return (ord(c) - ord(offset_char)) + 10
    else:
        return None
