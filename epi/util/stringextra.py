from collections import deque

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

def int_to_string(x, base=10):
    """
    Returns the string version of the integer x. Uses deque
    joining. The string is represented in base base.
    """

    if (not x):
        return "0"

    is_negative = False
    if (x < 0):
        x = -x
        is_negative = True

    answer = deque()
    while (x):
        answer.appendleft(int_to_digit(x % base))
        x //= base

    if (is_negative):
        answer.appendleft('-')

    return ''.join(answer)

def string_to_int(s, base=10):
    """
    Returns the integer version of the string x. s is
    represented in base base.
    """

    is_negative = False
    if (s[0] == '-'):
        s = iter(s)
        # skip first element
        next(s)
        is_negative = True

    answer = 0
    for c in s:
        answer = answer * base + digit_to_int(c)

    if (is_negative):
        answer = -answer
    return answer
