from hypothesis import given, settings
from hypothesis.strategies import integers
from nora_crypto import generate_keypair


@given(integers(min_value=1, max_value=2 ** 1024 - 1))
@settings(deadline=None)
def test_rsa_decryption(message: int):
    public, private = generate_keypair()

    # Make sure the message isn't too large for our keypair
    message %= public.n

    # Encrypt the message
    ciphertext = public.encrypt(message)

    # Decrypt the message
    plaintext = private.decrypt(ciphertext)

    assert plaintext == message

    # Sign the message
    signature = private.sign(message)
    assert public.verify(message, signature)


def test_rsa_brute_force():
    # Very weak key length so we can brute force it
    public, private = generate_keypair(bits=64)
    assert public.brute_force() == private
