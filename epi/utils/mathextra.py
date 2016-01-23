import fractions
import math
from epi.utils import itertoolsextra, python
from collections import namedtuple
from enum import Enum
from abc import ABCMeta, abstractmethod

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
    Return True if x is prime.

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
    while ((i**2) <= x):
        if (((x % i) == 0) or ((x % (i + 2)) == 0)):
            return False
        i += 6
    return True

def is_prime_sieve(x):
    """
    Return True if x is prime.

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
    Return the integer square root of x using Newton's method.

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

class AbstractPoint(metaclass=ABCMeta):
    """
    A 2-dimensional point on the Cartesian coordinates. This class also
    acts like a vector since it has methods such as __add__ and norm.

    The following point classes show how to use abstract classes and
    immutable classes. It gets messy with multiple inheritance so it would
    probably be better to allow a class to be mutable and implement a hash
    method but promise to treat the class as immutable if using hash.
    """

    @abstractmethod
    def __setattr__(self, name, value):
        """
        Abstract method so subclasses decide whether the point is mutable.
        """

        pass

    @abstractmethod
    def __delattr__(self, name):
        """
        Abstract method so subclasses decide whether the point is mutable.
        """

        pass

    def __init__(self, x, y):
        """
        Sets x and y using object's __setattr__() because this class'
        __setattr__() is overridden.
        """

        object.__setattr__(self, "x", x)
        object.__setattr__(self, "y", y)

    def shallow_copy(self,
                     x=python.Parameter.OTHER_ARGUMENT,
                     y=python.Parameter.OTHER_ARGUMENT):
        """
        Return a shallow copy of self. The type of object returned
        is the same as the type of self. If x or y is passed, set the x
        or y in the copy.
        """

        if (x is python.Parameter.OTHER_ARGUMENT):
            x = self.x
        if (y is python.Parameter.OTHER_ARGUMENT):
            y = self.y

        return self.__class__(x, y)

    """
    deep_copy is the same as shallow_copy because x and y are numbers,
    so they don't need to be deep copied.
    """
    deep_copy = shallow_copy

    def __add__(self, other):
        """
        Add other to self and return. Works like vector addition.
        """

        x = self.x + other.x
        y = self.y + other.y
        return self.shallow_copy(x, y)

    def __radd__(self, other):
        """
        Reverse add other to self and return.

        Checks if other == 0 to support sum() which starts with
        a sum of 0.
        """

        if other == 0:
            return self
        else:
            return self.__add__(other)

    def __sub__(self, other):
        """
        Subtract other from self and return.
        """

        x = self.x - other.x
        y = self.y - other.y
        return self.shallow_copy(x, y)

    def __mul__(self, other):
        """
        Multiply self by other and return. If other is a scalar,
        multiply x and y of self by other. If other is an AbstractPoint,
        multiply x and y of self by x and y of other respectively.
        """

        if (hasattr(other, "x") and hasattr(other, "y")):
            x = self.x * other.x
            y = self.y * other.y
        else:
            x = self.x * other
            y = self.y * other
        return self.shallow_copy(x, y)

    def __rmul__(self, other):
        """
        Reverse Multiply self by other and return.
        """

        return self.__mul__(other)

    def __truediv__(self, other):
        """
        Truediv self by other and return. If other is a scalar,
        truediv x and y of self by other. If other is an AbstractPoint,
        truediv x and y of self by x and y of other respectively.
        """

        if (hasattr(other, "x") and hasattr(other, "y")):
            x = self.x / other.x
            y = self.y / other.y
        else:
            x = self.x / other
            y = self.y / other
        return self.shallow_copy(x, y)

    def __floordiv__(self, other):
        """
        Floordiv self by other and return. If other is a scalar,
        floordiv x and y of self by other. If other is an AbstractPoint,
        floordiv x and y of self by x and y of other respectively.
        """

        if (hasattr(other, "x") and hasattr(other, "y")):
            x = self.x // other.x
            y = self.y // other.y
        else:
            x = self.x // other
            y = self.y // other
        return self.shallow_copy(x, y)

    def __abs__(self):
        """
        Return a copy of self with positive x and y.
        """

        return self.shallow_copy(abs(self.x), abs(self.y))

    def __neg__(self):
        """
        Return a copy of self with x and y negated.
        """

        return self.shallow_copy(-self.x, -self.y)

    def __pos__(self):
        """
        Return a copy of self.
        """

        return self.shallow_copy(self.x, self.y)

    def __eq__(self, other):
        """
        Return True if self is equal to other.

        __eq__(), _can_equal(), and _attributes_equal() should be
        overridden together.
        This works by having subclasses inherit this class' _can_equal()
        if it is not overridden. If _can_equal() is not overridden, that
        means the subclass is similar to a AbstractPoint so it uses
        AbstractPoint's _can_equal() and the subclass can be equal to a
        AbstractPoint.
        """

        return isinstance(other, AbstractPoint) and other._can_equal(self) and \
               self._attributes_equal(other)

    def _can_equal(self, other):
        """
        Return True if other can be equal to self.
        """

        return isinstance(other, AbstractPoint)

    def _attributes_equal(self, other):
        """
        Return True if all attributes of self and other are equal.
        """

        return (self.x == other.x) and (self.y == other.y)

    def __ne__(self, other):
        """
        Return True if self is not equal to other.
        """

        return not self.__eq__(other)

    def norm(self):
        """
        Return the norm (magnitude) of self as if it was a vector.
        """

        return math.sqrt(self.x**2 + self.y**2)

    def dot(self, other):
        """
        Return the dot product of self and other.
        """

        return (self.x * other.x) + (self.y * other.y)

    def is_close(self, other):
        """
        Return True if the two Abstract_Points are approximately
        equal to eachother.
        """

        return isinstance(other, AbstractPoint) and other._can_equal(self) and \
               self._attributes_close(other)

    def _attributes_close(self, other):
        return math.isclose(self.x, other.x) and \
               math.isclose(self.y, other.y)

    def is_orthogonal(self, other):
        """
        Return True if self is orthogonal to other.
        """

        check_value = self.dot(other)
        return (check_value == 0) or math.isclose(check_value, 0)

    def __repr__(self):
        """
        Return the representation of self. Looks like AbstractPoint(x=1, y=2).
        """

        return "{}(x={!r}, y={!r})".format(self.__class__.__name__, self.x, self.y)

    def __iter__(self):
        """
        Return an iterator of self.
        """

        yield x
        yield y

    class Region(Enum):
        """
        The part of the graph this point is on.
        """

        ORIGIN = 1
        POSITIVE_X = 2
        NEGATIVE_X = 3
        POSITIVE_Y = 4
        NEGATIVE_Y = 5
        QUADRANT1 = 6
        QUADRANT2 = 7
        QUADRANT3 = 8
        QUADRANT4 = 9

    @property
    def region(self):
        """
        Return the Region self is in.
        """

        if (self.x > 0):
            if (self.y > 0):
                return AbstractPoint.Region.QUADRANT1
            elif (self.y == 0):
                return AbstractPoint.Region.POSITIVE_X
            else: # self.y < 0
                return AbstractPoint.Region.QUADRANT4
        elif (self.x == 0):
            if (self.y > 0):
                return AbstractPoint.Region.POSITIVE_Y
            elif (self.y == 0):
                return AbstractPoint.Region.ORIGIN
            else: # self.y < 0
                return AbstractPoint.Region.NEGATIVE_Y
        else: # self.x < 0
            if (self.y > 0):
                return AbstractPoint.Region.QUADRANT2
            elif (self.y == 0):
                return AbstractPoint.Region.NEGATIVE_X
            else: # self.y < 0
                return AbstractPoint.Region.QUADRANT3

class FrozenPoint(AbstractPoint):
    """
    An immutable AbstractPoint. This class is immutable and subclasses
    should be immutable.
    """

    def __setattr__(self, *args):
        """
        Cannot set attributes because immutable.
        """

        raise TypeError("Cannot modify immutable instance")

    """
    Cannot delete attributes because immutable.
    """
    __delattr__ = __setattr__

    def __hash__(self):
        """
        Return self's hash.

        Hashable because immutable. If __eq__ is overridden, must
        override this as well. Equal points should have the same hash.
        """

        return hash((self.x, self.y))

    def __init__(self, x, y):
        """
        Initialize x, y, and _region to use as a cache for the region
        since it won't change for an immutable AbstractPoint.
        """

        super().__init__(x, y)
        object.__setattr__(self, "_region", None)

    @property
    def region(self):
        """
        Return and cache (if not already cached) the region self is in.
        """

        if (self._region is None):
            object.__setattr__(self, "_region", super().region)
        return self._region

class AbstractColoredPoint(AbstractPoint):
    """
    An AbstractPoint that has a color.

    This is an example class on how to create subclasses. This is also
    an abstract class liken AbstractPoint because it doesn't override
    __setattr__() and __delattr__().
    """

    def __init__(self, x, y, color):
        """
        Initialize x, y, and color for self.
        """

        super().__init__(x, y)
        object.__setattr__(self, "color", color)

    def shallow_copy(self,
                     x=python.Parameter.OTHER_ARGUMENT,
                     y=python.Parameter.OTHER_ARGUMENT,
                     color=python.Parameter.OTHER_ARGUMENT):
        """
        Return a shallow copy of self. The type of object returned
        is the same as the type of self. If x, y, or color is passed, 
        set the x, y, or color in the copy.
        """

        if (x is python.Parameter.OTHER_ARGUMENT):
            x = self.x
        if (y is python.Parameter.OTHER_ARGUMENT):
            y = self.y
        if (color is python.Parameter.OTHER_ARGUMENT):
            color = self.color

        return self.__class__(x, y, color)

    """
    deep_copy is the same as shallow_copy because x and y are numbers,
    so they don't need to be deep copied. Color doesn't have a representation
    yet but it can be a string. This is an example class so it isn't meant
    to be used.
    """
    deep_copy = shallow_copy

    def __eq__(self, other):
        """
        Return True if self is equal to other.
        """

        return isinstance(other, AbstractColoredPoint) and \
               other._can_equal(self) and \
               self._attributes_equal(other)

    def _can_equal(self, other):
        """
        Return True if other can be equal to self.
        """

        return isinstance(other, AbstractColoredPoint)

    def _attributes_equal(self, other):
        """
        Return True if all attributes of self and other are equal.
        """

        return super()._attributes_equal(other) and (self.color == other.color)

    def __repr__(self):
        return "{}(x={!r}, y={!r}, color={!r})".format(self.__class__.__name__,
                                                 self.x,
                                                 self.y,
                                                 self.color)

class FrozenColoredPoint(AbstractColoredPoint, FrozenPoint):
    """
    An AbstractColoredPoint that is frozen.
    """

    def __hash__(self):
        """
        Return self's hash.

        Hashable because immutable.
        """

        return hash((self.x, self.y, self.color))

class MutablePoint(AbstractPoint):
    """
    A Mutable AbstractPoint. This class is mutable and subclasses
    should be mutable.
    """

    def __setattr__(self, name, value):
        """
        Can set attributes because mutable.
        """

        object.__setattr__(self, name, value)

    def __delattr__(self, name):
        """
        Can delete attributes because mutable.
        """

        object.__delattr__(self, name)

    def __iadd__(self, other):
        """
        Add other to self. Works like vector addition.
        """

        self.x += other.x
        self.y += other.y
        return self

    def __isub__(self, other):
        """
        Subtract other from self.
        """

        self.x -= other.x
        self.y -= other.y
        return self

    def __imul__(self, other):
        """
        Multiply self by other. If other is a scalar,
        multiply x and y of self by other. If other is an AbstractPoint,
        multiply x and y of self by x and y of other respectively.
        """

        if (hasattr(other, "x") and hasattr(other, "y")):
            self.x *= other.x
            self.y *= other.y
        else:
            self.x *= other
            self.y *= other
        return self

    def __itruediv__(self, other):
        """
        Truediv self by other. If other is a scalar,
        truediv x and y of self by other. If other is an AbstractPoint,
        truediv x and y of self by x and y of other respectively.
        """

        if (hasattr(other, "x") and hasattr(other, "y")):
            self.x /= other.x
            self.y /= other.y
        else:
            self.x /= other
            self.y /= other
        return self

    def __ifloordiv__(self, other):
        """
        Floordiv self by other. If other is a scalar,
        floordiv x and y of self by other. If other is an AbstractPoint,
        floordiv x and y of self by x and y of other respectively.
        """

        if (hasattr(other, "x") and hasattr(other, "y")):
            self.x //= other.x
            self.y //= other.y
        else:
            self.x //= other
            self.y //= other
        return self

class MutableColoredPoint(AbstractColoredPoint, MutablePoint):
    """
    An AbstractColoredPoint that is mutable.
    """

    pass

class Rectangle:
    """
    An x-y aligned rectangle on the Cartesian coordinates.
    """

    def __init__(self, lower_left_point, width, height):
        """
        Create a Rectangle with a lower-left point and a width (x-axis)
        and height (y-axis). Width and height must be >= 0
        """

        self.lower_left_point = lower_left_point
        self.width = width
        self.height = height

    @property
    def width(self):
        return self._width

    @width.setter
    def width(self, value):
        if (value < 0):
            raise ValueError("width must be >= 0")
        else:
            self._width = value

    @property
    def height(self):
        return self._height

    @height.setter
    def height(self, value):
        if (value < 0):
            raise ValueError("height must be >= 0")
        else:
            self._height = value

    @classmethod
    def create_from_lower_left(cls, lower_left_point, width, height):
        """
        Create a Rectangle from the lower-left point.
        """

        return cls(lower_left_point, width, height)

    @classmethod
    def create_from_upper_right(cls, upper_right_point, width, height):
        """
        Create a Rectangle from the upper-right point.
        """

        lower_left_point = upper_right_point - FrozenPoint(width, height)
        return cls(lower_left_point, width, height)

    @classmethod
    def create_from_upper_left(cls, upper_left_point, width, height):
        """
        Create a Rectangle from the upper-left point.
        """

        lower_left_point = upper_left_point - FrozenPoint(0, height)
        return cls(lower_left_point, width, height)

    @classmethod
    def create_from_lower_right(cls, lower_right_point, width, height):
        """
        Create a Rectangle from the lower-right point.
        """

        lower_left_point = lower_right_point - FrozenPoint(width, 0)
        return cls(lower_left_point, width, height)

    @classmethod
    def create_from_points(cls, point0, point1):
        """
        Create a Rectangle starting from point0 to point1. The
        Rectangle created will contain these two points on opposite
        corners.
        """

        vector = point1 - point0
        width, height = abs(vector)

        vector_region = vector.region
        lower_left_create_regions = (Point.Region.ORIGIN,
                                     Point.Region.POSITIVE_X,
                                     Point.Region.POSITIVE_Y,
                                     Point.Region.QUADRANT1)
        lower_right_create_regions = (Point.Region.QUADRANT2,
                                      Point.Region.NEGATIVE_X)
        upper_right_create_regions = (Point.Region.QUADRANT3,
                                      Point.Region.NEGATIVE_Y)
        if (vector_region in lower_left_create_regions): 
            return cls.create_from_lower_left(point0, width, height)
        elif (vector_region in lower_right_create_regions):
            return cls.create_from_lower_right(point0, width, height)
        elif (vector_region in upper_right_create_regions):
            return cls.create_from_upper_right(point0, width, height)
        else: # (vector_region in Point.Region.QUADRANT4)
            return cls.create_from_upper_left(point0, width, height)

    @property
    def upper_right_point(self):
        """
        Return the upper-right point.
        """

        return self.lower_left_point + FrozenPoint(self.width, self.height)

    @property
    def upper_left_point(self):
        """
        Return the upper-left point.
        """

        return self.lower_left_point + FrozenPoint(0, self.height)

    @property
    def lower_right_point(self):
        """
        Return the lower-right point.
        """

        return self.lower_left_point + FrozenPoint(self.width, 0)

    @property
    def points(self):
        """
        Return a tuple of self's points from lower-left counter-clockwise
        ie. lower-left, lower-right, upper-right, upper-left.
        """

        return self.lower_left_point, self.lower_right_point, \
               self.upper_right_point, self.upper_left_point

    def intersects(self, rectangle):
        """
        Return True if self intersects with rectangle. This also considers
        the rectangles intersecting if they touch by a line or a point
        (0 area).

        This is explained easier with a diagram. I will only show the x-axis.
        The same applies to the y axis.

        The line segments below represent the rectangles projected on the
        x-axis. x0 is the x of the lower-left point, and x1 is the x of the
        upper-right point.
        Here are the possible cases for an intersection.

        Case 1, rectangle right of self:
        self:
        -------
        x0    x1

        rectangle:
             -----
             x0  x1

        Case 2, rectangle on top of self:
        self:
        -------
        x0    x1

        rectangle:
         -----
         x0  x1

        Case 3, rectangle left of self:
        self:
           -------
           x0    x1

        rectangle:
        -----
        x0  x1

        In all three cases, you see that self_x1 >= rectangle_x0 and
        rectangle_x1 >= self_x0
        These inequalities are symmetrical in that x1 >= x0. This shows
        that you can swap self and rectangle and the function still works.
        """

        self_p0 = self.lower_left_point
        self_p1 = self.upper_right_point
        rect_p0 = rectangle.lower_left_point
        rect_p1 = rectangle.upper_right_point

        return (self_p1.x >= rect_p0.x) and (rect_p1.x >= self_p0.x) and \
               (self_p1.y >= rect_p0.y) and (rect_p1.y >= self_p0.y)

    def intersection(self, rectangle):
        """
        Return the Rectangle formed from the intersection of self and
        rectangle. If there is no intersection, return None.

        The 0 and 1 suffix stands for the lower-left and upper-right points
        respectively.
        The reason we take the max for x0 and y0 and the min for
        x1 and y1 is described below.
        I will only describe it for the x. The same method can be
        applied for y.
        First we project the rectangle on the x-axis:
        self:
        -------
        x0    x1

        rectangle:
             -----
             x0  x1
        The intersection is to the right of x0, so we choose the max x0 as
        the intersection Rectangle's x0.
        The intersection is the left of x1, so we choose the min x1 as
        the intersection Rectangle's x1.
        """

        if (self.intersects(rectangle)):
            self_p0 = self.lower_left_point
            self_p1 = self.upper_right_point
            rect_p0 = rectangle.lower_left_point
            rect_p1 = rectangle.upper_right_point

            x = max(self_p0.x, rect_p0.x)
            y = max(self_p0.y, rect_p0.y)
            x1 = min(self_p1.x, rect_p1.x)
            y1 = min(self_p1.y, rect_p1.y)
            width = x1 - x
            height = y1 - y
            return Rectangle(FrozenPoint(x, y), width, height)
        return None

    def __eq__(self, other):
        """
        Return True if self is equal to other.
        """

        return isinstance(other, Rectangle) and \
               other._can_equal(self) and \
               self._attributes_equal(other)

    def _can_equal(self, other):
        """
        Return True if other can be equal to self.
        """

        return isinstance(other, Rectangle)

    def _attributes_equal(self, other):
        """
        Return True if all attributes of self and other are equal.
        """

        return (self.lower_left_point == other.lower_left_point) and \
               (self.width == other.width) and \
               (self.height == other.height)

    def __repr__(self):
        repr_string = "{}(lower_left_point={!r}, width={!r}, height={!r})"
        return repr_string.format(self.__class__.__name__,
                                                 self.lower_left_point,
                                                 self.width,
                                                 self.height)

    @staticmethod
    def is_rectangle(point0, point1, point2, point3):
        """
        Return True if point[0-3] are vertices of a rectangle.
        point[0-3] do not have to be xy-aligned.

        This works by checking if any of orderings of point[0-3] form a
        rectangle in that order. Only 3 orderings are checked because
        the others are repeats.

        For example, the rectangle below can be given in the orders
        Counter-clockwise: ABCD, BCDA, CDAB, DABC
        Clockwise: ADCB, DCBA, CBAD, BADC
        D_____C
        |     |
        |_____|
        A     B
        
        Another shape is
        Direction0: ADBC, DBCA, BCAD, CADB
        Direction1: ACBD, CBDA, BDAC, DACB
        D  C
        |\/|
        |/\|
        A  B

        The last shape is
        Direction0: ACDB, CDBA, DBAC, BACD
        Direction1: ABDC, BDCA, DCAB, CABD
        D____C
         \  /
          \/
          /\
         /__\
        A    B

        Given 4 points that form a rectangle, the ordering of the points
        will be one of the three shapes. Each shape has 8 orderings so
        we only need one for each shape. Only one of the shapes is a
        rectangle.
        """

        return Rectangle.is_rectangle_ordered(
                        point0, point1, point2, point3) or \
               Rectangle.is_rectangle_ordered(
                       point0, point2, point3, point1) or \
               Rectangle.is_rectangle_ordered(
                       point0, point3, point1, point2)

    @staticmethod
    def is_rectangle_ordered(point0, point1, point2, point3):
        """
        Return True if point[0-3] are vertices of a rectangle.
        point[0-3] should be ordered either clockwise or
        counter-clockwise. They do not have to be xy-aligned.

        For example, the rectangle below can be given in the orders
        Counter-clockwise: ABCD, BCDA, CDAB, DABC
        Clockwise: ADCB, DCBA, CBAD, BADC
        D_____C
        |     |
        |_____|
        A     B

        This works by checking that point[0-3] form a parallelogram and
        contains a right angle (checks angle point1-point0-point3).
        """

        answer = False
        if (Rectangle.is_parallelogram_ordered(point0, point1, point2, point3)):
            vector_01 = point1 - point0
            vector_03 = point3 - point0
            answer = vector_01.is_orthogonal(vector_03)
        return answer

    @staticmethod
    def is_parallelogram_ordered(point0, point1, point2, point3):
        """
        Return True if point[0-3] are vertices of a parallelogram.
        point[0-3] should be ordered either clockwise or counter-clockwise.

        For example, the parallelogram below can be given in the orders
        Counter-clockwise: ABCD, BCDA, CDAB, DABC
        Clockwise: ADCB, DCBA, CBAD, BADC
          D_____C
          /    /
         /____/
        A     B

        This works by checking that the vectors on opposite sides are
        equal starting from point0. This is a parallelogram
        because equal vectors are parallel and have the same magnitude.
        A quadrilateral is a parallelogram iff one pair of opposite sides
        are parallel and equal in length.
        """

        vector_01 = point1 - point0
        vector_32 = point2 - point3

        return (vector_01 == vector_32) or vector_01.is_close(vector_32)
