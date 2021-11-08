from hypothesis import given
from hypothesis.strategies import integers
from nora_crypto import is_prime_naive, is_prime_miller_rabin


def test_naive_prime_check():
    # Known primes up to 100
    known_primes = {2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97}

    for i in range(2, 100):
        assert is_prime_naive(i) == (i in known_primes)


@given(integers(min_value=2, max_value=int(1e12) - 1))
def test_miller_rabin_prime_check(n):
    assert is_prime_miller_rabin(n) == is_prime_naive(n)
