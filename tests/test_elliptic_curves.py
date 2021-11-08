from hypothesis import given
from hypothesis.strategies import integers, sampled_from
from nora_crypto import NIST_CURVES, EllipticCurve


@given(integers(), sampled_from(NIST_CURVES))
def test_group_closure(k: int, curve: EllipticCurve):
    # Points on the curve are closed under addition
    point = curve.generate_point(k)
    assert point in curve

    # Check for false positives
    assert point.perturb(0, 1) not in curve


@given(integers(), sampled_from(NIST_CURVES))
def test_identity_element(k: int, curve: EllipticCurve):
    point = curve.generate_point(k)
    assert point + curve.identity == curve.identity + point == point


@given(integers(), sampled_from(NIST_CURVES))
def test_inverse(k: int, curve: EllipticCurve):
    point = curve.generate_point(k)
    assert point + (-point) == curve.identity


# Very simple EC Diffie-Hellman key exchange test
@given(integers(), integers(), sampled_from(NIST_CURVES))
def test_key_exchange(secret1: int, secret2: int, curve: EllipticCurve):
    public1 = curve.generate_point(secret1)
    public2 = curve.generate_point(secret2)
    
    secret1 *= public2
    secret2 *= public1
    assert secret1 == secret2
