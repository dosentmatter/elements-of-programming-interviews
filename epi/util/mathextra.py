import fractions
from epi.util import itertoolsextra

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

def is_even(x):
    """
    Return True if x is even.
    """

    return (x & 1) == 0

def is_odd(x):
    """
    Return True if x is odd.
    """

    return (x & 1) == 1

def generate_primes(n):
    """
    Return a generator of prime numbers from [1, n].

    This works by doing the Sieve of Eratosthenes algorithm. It is
    optimized by skipping even elements when generating the sieve.
    By doing this optimization, there must be a conversion functions
    to convert from the sieve indices to what number it represents.

    Here are the 3 optimizations being done:
    1. The sieve does not represent 0, 1, 2, and even numbers.
    2. Start marking the sieve from prime_number * prime_number.
    3. When marking the sieve, only step an even amount so only odd
       numbers are marked.

    The optimization skips the first 3 elements, 0, 1, and 2 because
    0, and 1 are known non-primes and 2 is a known-prime. We skip
    all even numbers because they are known non-primes. I call
    the sieve the prime_boolean_list below.
    This means the conversion function is the following:
    number = (2 * index) + 3
    For example, index == 0 -> number == 3. This is correct as 0, 1, and 2
    are skipped.
    index == 1 -> number == 5. This is also correct as it is the next odd
    number.
    The inverse of the function is also true:
    index = (number - 3) // 2
    index will always be a whole number because number only represents
    odd numbers >= 3 as stated above.

    Here is an example of the mapping from index to number:
    prime_boolean_list indices:
    0, 1, 2, 3,  4,  5,  6
    number represented:
    3, 5, 7, 9, 11, 13, 15

    There is another optimization in the nested for loop range(). There
    is a start and step optimization.

    start optimization:
    Once you find a prime number in the outer loop, you start to mark
    numbers (prime_number * k) | k is a whole number
    Of course, k only increases until the max number represented in the
    sieve.
    The optimization is instead to do
    (prime_number * k) | k >= prime_number, k is a whole number
    This is because
    (prime_number * s) | 0 <= s < prime_number, s is a whole number
    has been marked in previous iterations by smaller prime numbers since
    s < prime_number.
    This optimization is why
    sieve_start_number == prime_number * prime_number
    Of course, we have to convert sieve_start_number to
    sieve_start_prime_boolean_index to index the sieve correctly.

    step optimization:
    All primes, besides 2, are odd because even numbers have a factor of 2.
    This means
    (prime_number * k) | k >= prime_number, k is a whole number
    can be optimized to
    (prime_number * k) | k >= prime_number, k is an odd whole number
    This is because (prime_number * k) is only odd if k is odd. All the
    even numbers are already marked (in this optimized version, they were
    all skipped so without this optimization, a fractional index would
    be indexed since even numbers don't exist in the sieve. Note that
    this fractional index would have been rounded down due to the use of
    // in number_to_prime_boolean_index) so we can skip them.

    The whole optmization is equivalent to:
    (prime_number * (prime_number + 2*k)) | k is a whole number
    or
    ((prime_number * prime_number) + 2*k*prime_number)) | k is a
    whole number
    From this, you can see that
    sieve_start_number == prime_number * prime_number
    and
    sieve_step_number_vector == 2 * p
    These have to be converted to prime boolean index and vectors
    respectively. sieve_step_number_vector is a vector because a step
    specifies a change in position (or index). Vectors are unaffected
    by shifts so number_vector_to_prime_boolean_vector is
    just number_prime_to_boolean_index without the -3 shift.
    """

    yield 2

    # these are inverse functions
    prime_boolean_index_to_number = lambda i: (2 * i) + 3
    number_to_prime_boolean_index = lambda n: (n - 3) // 2

    # vectors are unaffected by shifts
    number_vector_to_prime_boolean_vector = lambda nv: nv // 2

    prime_boolean_list_length = itertoolsextra.range_length(3, n + 1, 2)
    prime_boolean_list = [True] * prime_boolean_list_length
    for (i, is_prime) in enumerate(prime_boolean_list):
        if (is_prime):
            prime_number = prime_boolean_index_to_number(i)
            yield prime_number

            sieve_start_number = prime_number * prime_number
            sieve_start_prime_boolean_index = \
                    number_to_prime_boolean_index(sieve_start_number)

            sieve_step_number_vector = 2 * prime_number
            sieve_step_prime_boolean_vector = \
                number_vector_to_prime_boolean_vector(
                                            sieve_step_number_vector)

            for j in range(sieve_start_prime_boolean_index,
                           prime_boolean_list_length,
                           sieve_step_prime_boolean_vector):
                prime_boolean_list[j] = False

def is_prime(x):
    """
    Returns True if x is prime.

    This is a naive primality test. There are faster ones. This function
    uses the fact that all primes except 2 and 3 are 1 away from 6, so
    this checks if the numbers 5,6, 11,13, 17,19, etc. are factors of x.
    """

    if (x <= 1):
        return False
    elif (x <= 3):
        return True
    x_mod_6 = x % 6
    if ((x_mod_6 != 1) and (x_mod_6 != 5)):
        return False

    i = 5
    while ((i * i) <= x):
        if (((x % i) == 0) or ((x % (i + 2)) == 0)):
            return False
        i += 6
    return True

def is_prime_sieve(x):
    """
    Returns True if x is prime.

    This generates a sieve and iterates through all the primes generated
    by the sieve to check if they are factors of x. It is slower than
    the is_prime() function.
    """

    if (x <= 1):
        return False
    elif (x <= 3):
        return True
    x_mod_6 = x % 6
    if ((x_mod_6 != 1) and (x_mod_6 != 5)):
        return False

    sqrt_x = int_sqrt(x)
    for i in generate_primes(sqrt_x):
        if ((x % i) == 0):
            return False
    return True

def int_sqrt(x):
    """
    Returns the integer square root of x using Newton's method.

    This function starts with a guess of x and keeps updating
    the guess as long as it lowers. When it increases, it returns
    the previous guess.

    The guess formula comes form Newton's method. Here is the derivation:
    Let g0, g1 == guess, next_guess.
    Integer Newton's method:
    g1 = g0 - f(g0)//f'(g0)

    x is the input to this function.
    f(g) = g**2 - x
    f'(g) = 2g

    g1 = g0 - f(g0)//f'(g0)
    g1 = g0 - (g0**2 - x)//(2*g0)
    g1 = g0 + (x - g0**2)//(2*g0)
    g1 = g0 + (x//g0 - g0)//2
    g1 = (g0 + x//g0) // 2
    """

    if (x < 0):
        raise ValueError("math domain error")

    update = lambda guess: (guess + x//guess) // 2

    guess = x
    next_guess = update(guess)
    while (next_guess < guess):
        guess = next_guess
        next_guess = update(guess)
    return guess
