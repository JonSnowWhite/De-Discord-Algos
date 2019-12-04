def ChineseRemainderTheorem(a,m):
    """
    Calculates x such that x=a[i] mod m[i] for all i<len(min(a,m)) using the chinese remainder theorem.
    A and M have to be iterables of size at least 1.

    returns: x such that x=a[i] mod m[i] for all i<len(min(a,m))

    arguments:
            a: The remainders of the chinese remainder theorem
            m: The moduli of the chinese remainder theorem

    Exception:
            ValuError: Raised if either of the arguments a and m is not iterable
    """

    try:
        tmp = a[0]
        tmp = m[0]
    except:
        raise ValueError

    length = min(len(a),len(m))

    # Calculate the product M of all m_i's and M_i = M/m_i
    M = 1
    Mlist = []
    Nlist = []
    for i in range(length):
        M = M * m[i]
    for i in range(length):
        Mlist.append(M/m[i])

        # Calculate the Inverse N_i of M_i mod m_i which we know must exist as M_i is co-prime to m_i
        Nlist.append(inverse_modulo(Mlist[i],m[i]))
    
    # Calculate the result x = sum(a[i]*M_i*N_i)
    # We know that one summand will only be a_i for the modulus m_i
    x = 0
    for i in range(length):
        tmp = (Mlist[i] * Nlist[i]) % M
        tmp = (tmp * a[i]) % M
        x = (x + tmp) % M
    return x

def CRT(a,m):
    return ChineseRemainderTheorem(a,m)