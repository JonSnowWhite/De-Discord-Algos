def square_and_multiply(base, modulo, exponent, verbose = False):
    """ Calculates base^(exponent) mod modulo (g^e) mod p with the shift and multiply algorithm.

    returns: base^(exponent) mod modulo (int)

    arguments:
            base: The base of the calculation. Has to be smaller than the modulo (int)
            modulo: The modulo of the calculation. The result will certainly be smaller than this (int)
            exponent: The exponent of the calculation.
            verbose: If true this function will print intermediate calculation

    runtime:
            Assuming multiplication n*m has runtime O(n+m) the multiplications
            in this algorithm are bounded by O(modulo) as the base is always
            smaller than the modulo. Per shift_and_multiply cycle two (or one)
            multiplications are done. The number of cycles is log(exponent),
            leaving us with a total runtime of O(log(exponent)*modulo). In a
            practical environment, where the modulo is bound by a constant this
            algorithm only has runtime O(log(exponent)), which is much more
            efficient than an intuitive approach.
    """
    if base > modulo:
        base = base % modulo
    if exponent == 0:
        return 1
    g = base  # translate values into commonly used variables
    p = modulo
    e = exponent
    e_bin_str = bin(exponent)[2:] # format the exponent into a binary string
    e_bin = [i for i in e_bin_str[1:]]  # and a list representation of the string
    y = g # skip the first one in the exponent as it will always be there
    if verbose:
        print("Exponent e = " + str(e) + " = " + e_bin_str + "_2")
        print("Base g = " + str(g)) # intermediate results
        print("Modulo p = " + str(p))
        print(str(g) + "^(1) mod " + str(p) + " = " + str(g))
    for i in range(0,len(e_bin)): #iterate over all binary digits of the exponent
        #log(exponent) steps
        shift_and_multiply = '    Square'
        y = y**2 % p # square y as it equals doubling/shifting the exponent of g
        if (e_bin[i]) == '1':
            y = y*g % p # multiply with g as this is equals to adding a one in the exponent of g
            shift_and_multiply += " and multiply"
        if verbose:
            print(str(g) + "^(" + e_bin_str[:i+2] + ") mod " + str(p) + " = " + str(y) + shift_and_multiply)

    if verbose:
        print("Solution:" + str(y))
    return y
