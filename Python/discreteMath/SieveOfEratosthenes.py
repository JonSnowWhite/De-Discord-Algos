def sieve_of_eratosthenes(b):
    """
    Calculates all primes up to and including b
    """
    primes = []
    # 0 and 1 are not prime
    prime_index = [False,False]+(b-1)*[True]
    for i in range(2,len(prime_index)):
        # in this case we found a prime
        if prime_index[i]:
            primes.append(i)
            # eliminate all multiples of this number as possible primes
            for j in range(i*i,len(prime_index),i):
                prime_index[j] = False
    return primes
