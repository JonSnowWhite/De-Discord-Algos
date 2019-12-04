import math

def BabyStepGiantStep(group, a, b):
    """
    Solves the disrete logarithm problem in groups that 
    extend the AbstGroup class. For a group of order g this
    algorithm has a runtime of O(sqrt(g)) and calculats x
    such that a^x = b in the given group.

    returns: x, such that a^x = b in the given group

    arguments:
            a: The base of a^x = b
            b: The result of a^x = b
            group: The group in which the result will be calculated
    """
    order = group.order()
    # we calculate the square root of the order of the group to 
    # balance time complexity against space complexity
    m = int(math.ceil(math.sqrt(order)))
    table = dict()
    # save the first sqrt(order) members of the group together with their exponents
    for j in range(0,m):
        exponent = group.exp(a,j)
        table[exponent] = j
    # take steps of size sqrt(order) to not be able to miss our sqrt(order) pre-calcuated elements
    stepsizemult = group.exp(a,group.inv(m))
    foot = b
    # with our foot (element) we take steps of size sqrt(order) until we find one of the precalculated elements
    # from there we can recalculate the original x such that a^x=b
    for i in range(0,m):
        try:
            return table[foot]
        except KeyError:
            foot = group.op(foot,stepsizemult)

def BSGS(group,a,b):
    return BabyStepGiantStep(group,a,b)

def loginv(group,a,b):
    return BabyStepGiantStep(group,a,b)