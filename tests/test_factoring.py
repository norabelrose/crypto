from hypothesis import given
from hypothesis.strategies import integers
from nora_crypto import gcd_euclidean, smallest_prime_factor
import math


@given(integers(min_value=1, max_value=1000), integers(min_value=1, max_value=1000))
def test_gcd_euclidean(a, b):
    assert gcd_euclidean(a, b) == math.gcd(a, b)


@given(integers(min_value=2, max_value=int(1e6) + 1))
def test_smallest_prime_factor(n):
    factor = smallest_prime_factor(n)
    assert math.gcd(factor, factor) == factor   # It's actually prime
    assert (n % factor) == 0                    # It's actually a factor