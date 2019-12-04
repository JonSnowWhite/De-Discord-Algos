from abc import ABCMeta, abstractmethod
import numpy

from ..discreteMath.SquareAndMultiply import square_and_multiply
from ..discreteMath.ExtendedEuklidianAlgorithm import inverse_modulo
from subprocess import check_output

class AbstGroup:
    """
    Abstract Group class.
    """

    __metaclass__ = ABCMeta
    
    # this must be set by the implementing classes construtor
    neutral_element = None

    @abstractmethod
    def op(self,a,b):
        """
        Should implement the group operation on two arbitrary elements
        """
        pass

    @abstractmethod
    def inv(self,element):
        """
        Should implement the inverse element of the given element in the group.
        """
        pass

    def exp(self,element, exponent):
        """
        Should implement the exponentation of one element to a certain power. While this 
        implementation works it can be overwritten to be faster in different groups.
        """
        if exponent == 0:
            return self.neutral_element
        
        ret = element
        for i in range(exponent-1):
            ret = op(element,element)
        return ret
    

    def order(self):
        """
        Returns the order of the group (i.e. the amount of elements
            in the group). Must be overwritten.
        """
        return 1

class MultModGroup(AbstGroup):
    """
    Implements a group over multiplication modulo N.
    """

    def __init__(self,N):
        """
        Sets the modulo of the multiplicative group to N and specifies 1 as the neutral element.
        """
        self.neutral_element = 1
        self.N = N
    
    def op(self,a,b):
        a = a % N
        b = b % N
        return (a*b) % self.N

    def exp(self,element, exponent):
        return square_and_multiply(element, self.N, exponent)

    def inv(self, element):
        return inverse_modulo(element, self.N)

    def order(self):
        return self.N


class EllCurveGroup:
    """
    Implements an elliptic curve mod N group. 
    All (x,y) such that
    y^2 = x^3 + ax + b % N
    are members of the group.
    We refer to the op(a,b) function for description of the group operation
    """

    def __init__(self,a,b,N):
        """
        Sets the parameters that describe the curve
        y^2 = x^3 + ax + b % N
        and the neutral element as the point in infinity: None
        """
        self.a = a
        self.b = b
        self.N = N
        self.neutral_element = None

    def op(a,b):
        """
        Calculates the point addition on the curve specified by a and b.
        It is important that a and b are tuples with two valid coordinates.
        """
        N = self.N

        if len(a) != 2 or len(b) != 2:
            raise Exception
        
        x1 = a[0]
        y1 = a[1]
        x2 = b[0]
        y2 = b[1]

        # one of the elements is the neutral element
        if a == self.neutral_element:
            return b
        if b == self.neutral_element:
            return a
        
        # the edge connecting a and b goes straight up
        if x1 == x2 and y1 != y2:
            return self.neutral_element
        
        # the tangent is infinity
        if x1==x2 and y1 == 0 and y2 == 0:
            return self.neutral_element
        
        # different points so point addition
        if x1 != x2 or y1 != y2:
            temp = ((y2-y1)*inverse_modulo((x2-x1),N)) % N
        # same points so point doubling
        if x1 == x2 and y1 == y2:
            temp = (((3*(x2**2 % N) + a) % N) * inverse_modulo(2*y2,N)) % N

        x3 = (temp**2-x1-x2) % N
        y3 = (temp*(x2-x3)-y2) % N
        return (x3,y3)

    def exp(self, element, exponent):
        """
        Returns the exponentation of an element by an exponent in the elliptic curve group by
        using the group operation point addition often enough.
        """
        super.exp(self,element,exponent)

    def inv(self, element):
        """
        Returns the inverse element of the elliptic curve by reflecting it on the x-axis.
        """
        try:
            return ((-1) * element[0],element[1])
        except:
            raise ValueError

    # TODO: PORT LIBRARY TO PYTHON2 such that we can use it here
    def order(self):
        """
        Returns the order of the elliptic curve group using another library. Unfortunately that library requires 
        python3 to be installed on the system.
        """
        out = check_output(["python3", "pyschoof/naive_schoof.py", str(self.N), str(self.a), str(self.   b)])
        return int(out)

