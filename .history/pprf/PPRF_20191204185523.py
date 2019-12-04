from abc import ABCMeta, abstractmethod

import ..discreteMath/SquareAndMultiply as sqm
from Crypto.PublicKey import RSA
from Crypto.Random import random
from Crypto.Hash import SHAKE256
import struct

class PuncturedException(ValueError):
    """
    Exception that is thrown if a punctured value is evaluated in a PPRF.
    """
    def __init__(self, arg = ''):
        self.strerror = arg
        self.args = {arg}

class AbstPPRF:
    """
    This class models a PuncturablePseudoRandomFunction. A PPRF is a normal function F: X->Y. But,
    one can make it unevaluatable for a certain value without affecting any other value. It basically
    implements the PPRF as introduced in 'Session Resumption Protocols and Efficient Forward Security
    for TLS 1.3 0-RTT' The research group around Tibor Jager created a C implementation in OpenSSL of
    this to show its practical fuctionality. This is a much simpler python implementation of such a 
    function for any purpose.

    The PPRF offers three functions:

    setup(secpem): Initializes the function with a certain security parameter which will define the 
        'grade of security' of the function. As of end of 2019, 4096 is recommended. In practice this
        function will be the constructor.
    
    evaluate(x): Evaluates the PPRF on value x, iff x is a member of X. Meaning, if will only evaluate it
        for valid x. Furthermore, the PPRF will not return a results if the value x has been punctured.

    puncture(x): Punctures the PPRF on value x. That means that the evaluate(x) will not be able to return a
        result anymore. Even more so, should all data about the PPRF be leaked no one can find te result of
        evaluate(x) in acceptable time regarding to the security parameter.
    """

    __metaclass__ = ABCMeta

    secpem = 0

    def __init__(self,secpem):
        """
        Initializes the PPRF with secpem as its security parameter.

        Arguments:
            secpem: Security parameter of the PPRF. Must be larger than 2048 for security purposes and divisible by 8(int)
        
        Exception:
            ValueError: Should secpem be smaller than 2048 or not divisible by 8.
        """
        if secpem < 2048 or secpem % 8 != 0:
            raise ValueError("secpem has to be at least 2048 and divisible by 8")
        else:
            self.secpem = secpem
    
    @abstractmethod
    def evaluate(self,x):
        """
        Returns the y in Y of x in X of the PPRF F: X->Y. It will return an exception should x be a punctured value
        or not in the defined range of the PPRF F.

        Arguments:
            x: The value for which F(x) will be returned
        
        Exception:
            PuncturedException: Should F(x) be punctured.
            ValueError: Should x not be member of X in F: X->Y
        """
    
    @abstractmethod
    def puncture(self,x):
        """
        Punctures the PPRF F on value x. Making in unevaluatable both for callers of the evaluate function and anyone
        that gets access to the raw data of the PPRF.

        Arguments:
            x: The value for which F will be punctured.

        Exception:
            ValueError: Should x not be member of X in F: X->Y
        """

class InnerPPRF:
    """
    An instantiation of a PPRF that uses the strong RSA assumption for security. How the PPRF works will be explained 
    here, for security proof and further reading we refer to 'Session Resumption Protocols and Efficient Forward Security for TLS 1.3 0-RTT'.

    Contains 232 values.
    """

    punctures = []
    g = 0
    outerPPRF = None

    def __init__(self,outerPPRF):
        """
        Constructor of the InnerPPRF. 

        Arguments: 
            outerPPRF: the outerPPRF with the modulo value. needed for this innerPPRF.
        """
        self.outerPPRF = outerPPRF

        self.g = random.randint(0,self.outerPPRF.N-1)

    def evaluate(self,x):
        """
        Returns the y in Y of x in X of the PPRF F: X->Y. It will return an exception should x be a punctured value
        or not in the defined range of the PPRF F.

        Arguments:
            x: The value for which F(x) will be returned
        
        Exception:
            PuncturedException: Should F(x) be punctured.
            ValueError: Should x not be member of X in F: X->Y
        """
        if x in self.punctures:
            raise PuncturedException
        if x<0 or x>231:
            raise ValueError

        mult = 1
        for j in range(len(self.outerPPRF.primes)):
            if (j!=x) and not (j in self.punctures):
                mult *= self.outerPPRF.primes[j] % self.outerPPRF.N
        ret = sqm.square_and_multiply(self.g,self.outerPPRF.N,mult)
        hash = SHAKE256.new()
        hash.update(ret.to_bytes(int(self.outerPPRF.secpem/8),'little'))
        return hash.read(int(self.outerPPRF.secpem/8))

    def puncture(self,x):
        """
        Punctures the PPRF F on value x. Making in unevaluatable both for callers of the evaluate function and anyone
        that gets access to the raw data of the PPRF.

        Arguments:
            x: The value for which F will be punctured.

        Exception:
            ValueError: Should x not be member of X in F: X->Y
        """
        if x in self.punctures:
            return
        if x<0 or x>231:
            raise ValueError

        self.g = sqm.square_and_multiply(self.g,self.outerPPRF.N,self.outerPPRF.primes[x])
        self.punctures.append(x)
        return

class OuterPPRF(AbstPPRF):
    """
    An instantiation of a PPRF that uses the strong RSA assumption for security. How the PPRF works will be explained 
    here, for security proof and further reading we refer to 'Session Resumption Protocols and Efficient Forward Security for TLS 1.3 0-RTT'.

    Contains a list of smaller PPRFs that each have 232 values. Mostly catches errors and delegates the functions to the
    correct innerPPRF.
    """


    # the first 232 uneven prime numbers
    primes = [3,5,7,11,13,17,19,23,29,31,37,41,43,47,53,59,61,67,71,73,79,83,89,97,101,103,107,109,113,127,131,137,139,149,151,157,163,167,173,179,181,191,193,197,199,211,223,227,229,233,239,241,251,257,263,269,271,277,281,283,293,307,311,313,317,331,337,347,349,353,359,367,373,379,383,389,397,401,409,419,421,431,433,439,443,449,457,461,463,467,479,487,491,499,503,509,521,523,541,547,557,563,569,571,577,587,593,599,601,607,613,617,619,631,641,643,647,653,659,661,673,677,683,691,701,709,719,727,733,739,743,751,757,761,769,773,787,797,809,811,821,823,827,829,839,853,857,859,863,877,881,883,887,907,911,919,929,937,941,947,953,967,971,977,983,991,997,1009,1013,1019,1021,1031,1033,1039,1049,1051,1061,1063,1069,1087,1091,1093,1097,1103,1109,1117,1123,1129,1151,1153,1163,1171,1181,1187,1193,1201,1213,1217,1223,1229,1231,1237,1249,1259,1277,1279,1283,1289,1291,1297,1301,1303,1307,1319,1321,1327,1361,1367,1373,1381,1399,1409,1423,1427,1429,1433,1439,1447,1451,1453,1459,1471]
    values = 0
    innerPPRFs = []
    # modulus needed in the innerPPRFs. Can be safely shared
    N = 0

    def __init__(self,secpem,values):
        """
        Initializes the PPRF with secpem as its security parameter.

        Arguments:
            secpem: Security parameter of the PPRF. Must be larger than 2048 for security purposes and divisible by 8(int)
            values: Number of values the function will be able to map. Size of X in F: X->Y. Must be larger than 231
            and a multiple of 232(int)
        
        Exception:
            ValueError: Should secpem be smaller than 2048 or not divisible by 8 or
                        should values be smaller than 232 or not divisible by 232.
        """
        super(OuterPPRF, self).__init__(secpem)
        if values < 232 or values % 232 !=0:
            raise ValueError("values has to be at least 232 and divisible by 232")
        self.values = values

        key = RSA.generate(self.secpem)
        self.N = key.n
        
        for i in range(int(values/232)):
            self.innerPPRFs.append(InnerPPRF(self))
    
    def evaluate(self,x):
        """
        Returns the y in Y of x in X of the PPRF F: X->Y. It will return an exception should x be a punctured value
        or not in the defined range of the PPRF F.

        Arguments:
            x: The value for which F(x) will be returned
        
        Exception:
            PuncturedException: Should F(x) be punctured.
            ValueError: Should x not be member of X in F: X->Y
        """
        if x >= self.values:
            ValueError
        
        # Choose the right PPRF and its index
        innerpprf = int(x / 232);
        innerpprf_index = x % 232;
        return self.innerPPRFs[innerpprf].evaluate(innerpprf_index)
    
    def puncture(self,x):
        """
        Punctures the PPRF F on value x. Making in unevaluatable both for callers of the evaluate function and anyone
        that gets access to the raw data of the PPRF.

        Arguments:
            x: The value for which F will be punctured.

        Exception:
            ValueError: Should x not be member of X in F: X->Y
        """
        if x >= self.values:
            raise ValueError
        
        # Choose the right PPRF and its index
        innerpprf = int(x / 232);
        innerpprf_index = x % 232;
        return self.innerPPRFs[innerpprf].puncture(x)
    