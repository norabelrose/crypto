import math


# Naive Euclidean algorithm for finding the greatest common divisor of two numbers
def gcd_euclidean(a: int, b: int) -> int:
    while b != 0:
        a, b = b, a % b
    
    return a


# Naive algorithm for finding the smallest prime factor of a number
def smallest_prime_factor(n: int):
    assert n > 1
    
    # For even numbers, the smallest prime factor is trivially 2
    if n % 2 == 0:
        return 2
    
    # Now we can just check the odd numbers up to sqrt(n), inclusive
    for i in range(3, int(math.sqrt(n)) + 1, 2):
        if n % i == 0:
            return i
    
    return n    # n is prime