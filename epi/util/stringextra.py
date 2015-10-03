from collections import deque

def int_to_digit(x):
    """
    Returns the digit version of the integer x. The digit is represented
    as a length-1 string (a character).
    Supports up to base36 digits. Alphabetical digits are lowercase.
    """

    if (x < 0):
        raise ValueError("x is negative.")
    elif (x < 10): # 0 to 9
        return chr(ord('0') + x)
    elif (x < 36): # a to f
        return chr(ord('a') + (x - 10))
    else:
        raise ValueError("x is >= 36.")

def digit_to_int(c):
    """
    Returns the integer version of the digit c. c is represented as a length-1
    string (a character).
    Supports up to base36 digits. Accepts uppercase and lowercase alphabetical
    digits.
    """

    if (c.isdigit()):
        return ord(c) - ord('0')
    elif (c.isalpha()):
        offset_char = 'a'
        if (c.isupper()):
            offset_char = 'A'
        return (ord(c) - ord(offset_char)) + 10
    else:
        raise ValueError("c is not a digit, [a-z], or [A-Z].")

def int_to_string(x, base=10):
    """
    Returns the string version of the integer x. Uses deque
    joining. The string is represented in base base.
    Alphabetical digits are lowercase. Accepts bases in the range
    [2, 36].
    """

    if ((base < 2) or (base > 36)):
        raise ValueError("base must be >= 2 and <=36")

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

def int_to_string_python(x, base=10):
    """
    Returns the string version of the integer x using Python's bin(),
    oct(), and hex() when possible. Uses deque joining. The string
    is represented in base base.
    Alphabetical digits are lowercase. Accepts bases in the range
    [2, 36].
    """

    if ((base < 2) or (base > 36)):
        raise ValueError("base must be >= 2 and <=36")

    if (not x):
        return "0"

    DROP_PREFIX_INDEX = 2
    if (base == 2):
        return bin(x)[DROP_PREFIX_INDEX:]
    elif (base == 8):
        return oct(x)[DROP_PREFIX_INDEX:]
    elif (base == 16):
        return hex(x)[DROP_PREFIX_INDEX:]

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
    Returns the integer version of the string x. base is the base
    s is represented in.
    Alphabetical digits are lowercase or uppercase. Accepts bases
    in the range [2, 36].
    """

    if ((base < 2) or (base > 36)):
        raise ValueError("base must be >= 2 and <=36")

    is_negative = False
    if (s[0] == '-'):
        s = iter(s)
        # skip first element
        next(s)
        is_negative = True

    answer = 0
    for c in s:
        integer = digit_to_int(c)
        if (integer >= base):
            raise ValueError("s contains digit >= base.")
        answer = answer * base + integer

    if (is_negative):
        answer = -answer
    return answer

def string_to_int_python(s, base=10):
    """
    Returns the integer version of the string x using Python's int().
    base is the base s is represented in.
    Alphabetical digits are lowercase or uppercase. Accepts bases
    in the range [2, 36].
    """

    return int(s, base)

def column_id_digit_encode(x):
    """
    Returns the column id digit of the integer x. The column id digit
    is represented as a length-1 string (a character).
    Supports up to 26 column ids [a-z]. Column ids will be lowercase.
    """

    if (x < 1):
        raise ValueError("x is < 1.")
    elif (x <= 26): # a to z
        return chr(ord('a') + (x - 1))
    else:
        raise ValueError("x is > 26.")

def column_id_digit_decode(c):
    """
    Returns the integer version of the column id c. c is represented
    as a length-1 string (a character).
    Supports up to 26 column ids [a-z]. Accepts uppercase and lowercase
    column ids.
    """

    if (c.isalpha()):
        offset_char = 'a'
        if (c.isupper()):
            offset_char = 'A'
        return (ord(c) - ord(offset_char)) + 1
    else:
        raise ValueError("c is not [a-z] or [A-Z].")

def elias_gamma_encode(x):
    """
    Returns the Elias gamma encoding of the integer x as a string.
    """

    binary_x = int_to_string(x, 2)
    return binary_x.zfill(len(binary_x) - 1)

def elias_gamma_decode(s):
    """
    Returns the Elias gamma decoding of the string s as an integer.
    s
    """

    binary_number_start = s.index('1')
    number_leading_zeros = binary_number_start_index
    binary_number_end = binary_number_start + (number_leading_zeros + 1)

    x = s[binary_number_start:binary_number_end]
    return string_to_int(x, 2)
