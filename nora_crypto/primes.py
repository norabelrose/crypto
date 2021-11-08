import math


# Naive algorithm for testing primality, O(sqrt(n))
def is_prime_naive(n: int):
    # Negative numbers, zero, and one are not prime
    if n <= 1:
        return False
    
    # Two is the only even prime number
    if n == 2:
        return True
    
    # All other even numbers are not prime
    if n % 2 == 0:
        return False
    
    # Now we can just check the odd numbers up to sqrt(n), inclusive
    for i in range(3, int(math.sqrt(n)) + 1, 2):
        if n % i == 0:
            return False
    
    return True


# Miller-Rabin algorithm for testing primality. In principle, this is a probabilistic algorithm,
# so it may return false positives. However the probability of a false positive is equal to
# (1/4)^k, where k is the number of iterations, so it is negligibly likely to happen.
def is_prime_miller_rabin(n: int, rounds: int = 64):
    # Same trivial checks as naive algorithm
    if n <= 1:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False
    
    # Any odd number n can be written as n = 2^s * d + 1, where d is odd
    s = 0
    d = n - 1           # With s = 0, d = n - 1, the above equation does hold except that d is not odd
    while d % 2 == 0:   # Keep dividing d by 2 until it's odd, "moving" the factors of 2 into 2^s
        d //= 2
        s += 1
    
    for a in range(2, min(n - 2, rounds)):
        x = pow(a, d, n)
        if x == 1 or x == n - 1:
            continue
        for r in range(1, s):
            x = pow(x, 2, n)
            if x == 1:
                return False
            if x == n - 1:
                a = 0
                break
        if a:
            return False
    
    return True


# Returns N if it is prime, otherwise returns the next prime number after N.
def next_prime(n: int):
    # Make sure it's odd
    n |= 1

    # Check if it's prime. If it's composite, try the next odd number.
    while not is_prime_miller_rabin(n):
        n += 2
    
    return n
