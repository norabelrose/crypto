from collections import namedtuple
from typing import Tuple
from .factoring import smallest_prime_factor
from .primes import next_prime
import secrets


class RSAPublicKey(
        namedtuple('_RSAPublicKey', ['e', 'n'])
    ):
    def brute_force(self) -> 'RSAPrivateKey':
        p = smallest_prime_factor(self.n)
        q = self.n // p

        phi = (p - 1) * (q - 1)
        d = pow(self.e, -1, phi)
        return RSAPrivateKey(d, self.n)

    def encrypt(self, m: int) -> int:
        assert m < self.n, "Plaintext must be less than n"
        return pow(m, self.e, self.n)
    
    def verify(self, m: int, signature: int) -> bool:
        return pow(signature, self.e, self.n) == m


class RSAPrivateKey(
        namedtuple('_RSAPrivateKey', ['d', 'n'])
    ):
    def decrypt(self, c: int) -> int:
        return pow(c, self.d, self.n)
    
    # Digitally signing a message is the same as "decrypting" the plaintext with the private key.
    sign = decrypt


def generate_keypair(bits: int = 1024) -> Tuple[RSAPublicKey, RSAPrivateKey]:
    assert bits % 8 == 0, "`bits` must be a multiple of 8"

    # Select p and q to have slightly different bit lengths (we choose p to be the smaller one)
    length_delta = 3    # Arbitrary interpretation of the word 'few' in the original paper
    p = next_prime(secrets.randbits(bits // 2 - length_delta))
    q = next_prime(secrets.randbits(bits // 2 + length_delta))
    n = p * q

    # Here we use Euler's totient function (the number of positive integers less than n that are coprime to n),
    # which by construction is equal to (p - 1) * (q - 1) in this case because p and q are both prime. Essentially,
    # we are just removing any multiples of p or q from the set of positive integers less than n.
    phi = (p - 1) * (q - 1)

    # Really e just needs to be *some* integer 1 < e < phi which is coprime to phi. But since this is going to be
    # part of the public key, we don't care about randomness and can use any convenient constant. Smaller values
    # of e result in faster encryption, and since 2 ** 16 + 1 is known to be prime we know gcd(e, phi) == 1.
    # See https://crypto.stanford.edu/~dabo/pubs/papers/RSA-survey.pdf page 6 for more details.
    e = 2 ** 16 + 1
    
    # Compute the modular multiplicative inverse of e (mod phi). This is the private key.
    # Phi, which is used to compute d, must also be kept private or destroyed.
    d = pow(e, -1, phi)
    return RSAPublicKey(e, n), RSAPrivateKey(d, n)