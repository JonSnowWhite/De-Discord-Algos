def extended_euklidian_algorithm(a, b):
    """Calculates the greatest common divisor of a and b and s and t of the
     formula ggT(a,b) = s*a+b*t with the extended euklidian algorithm

     Arguments:
            a: first number of the gcd (int)
            b: second number of the gcd (int)

    Return:
            a tuple of the greatest common divisor of a and b as an integer and
            the tuple (s,t)

    Exception:
            ArithmeticError: if numbers smaller than 1 are entered
    """
    if a < 1 or b < 1:
        raise ArithmeticError

    table = [] # table with 5 columns and as much rows as the algorithm has
               # iterations, colums are a, b, a//b, None, None after the
               # normal euklidian algorithm has run once, with a and b being
               # the two numbers calcluating the modulo of


    if b > a:   #swap so a is always bigger or equal to b
        a,b = b,a

    c = 2
    while c != 1 and c != 0:
        q = a // b
        row = (a, b, q , None, None)
        table.append(row)
        c = a % b
        a = b
        b = c
    if b == 1: #a and b are relative prime and the gcd is 1
        table.append((a, 1, None, 0, 1))
        ggt = 1
    if b == 0: #a and b have a gcd a
        table.append((a, 0, None, 1, 0))
        ggt = a

    #here starts the extended euklidian algorithm that fills the table

    for i in range(len(table) - 2, -1, -1):  # iterate over the tale rows reverse
                                            # and without the last row
        row = table[i]
        last_row = table[i + 1]
        a = row[0]
        b = row[1]
        q = row[2]
        s = last_row[3]
        t = last_row[4]
        table[i] = (a, b, q, t, s-q*t)
        last_row = row

    # return ggt(a,b) and a tuple (s,t) such that ggT = s*a+t*b mind that a>b!
    return (ggt, (table[0][3], table[0][4]))

def inverse_modulo(a, p):
    """
    Calculates the inverse of a regarding modulo p with the extended extended
    euklidian Algorithm

    arguments:
            a: the number to calculate the reverse of (int)
            p: the modulo of the inverse operation (int)

    returns:
            a^(-1) mod p (int)

    throws:
            ArithmeticError: if a and p are not coprime i.e ggT(a,p)=/=1
    """
    a = a % p

    euklid = extended_euklidian_algorithm(a,p)
    if euklid[0] != 1:
        raise ArithmeticError
    return euklid[1][1] % p

def eea(a,b):
    return extended_euklidian_algorithm(a,b)