# from ExtendedEuklidianAlgorithm import *
# from SquareAndMultiply import *
# from ChineseRemainderTheorem import *


def allPerms(values):
    """
    A generator that yields all permutations of the values in values. 

    Params:
        valus: Must be an iterable object. All permutations of its content are yielded (Iterable)

    Yields:
        The next permutation of the values in values
    
    Raises:
        ValueError: Should values not be iterable
    """
    try:
        values = iter(values)
    except:
        raise ValueError("Parameter values must be Iterable")

    values = list(values)


    def innerAllPerms(setvalues,values):
        """
        Inner function that yields all permutations of the given values recursively.

        One recursive call sets one more value of the current permutation and calls itself recursively 
        to permutate over the rest. If only one value is left to permutate over the permutation is yielded and 
        other values are set by the calling function.
        """
        if len(values)==1:
            ret = setvalues[:]
            ret.append(values[0])
            yield ret
        elif len(values)==0:
            # only happens if the initial values were an empty iterator
            yield []
        else:
            # take from the front and append back at the end
            # this way we can circumvent iteration while working on the list
            unsetvalues = len(values)
            for i in range(unsetvalues):
                setvalues.append(values.pop(0))
                yield from innerAllPerms(setvalues,values)
                values.append(setvalues.pop(len(setvalues)-1))

    yield from innerAllPerms([],values)