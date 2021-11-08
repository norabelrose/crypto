from dataclasses import dataclass
from typing import Tuple


# y^2 = x^3 + ax + b (mod p)
@dataclass(frozen=True)
class EllipticCurve:
    a: int
    b: int
    p: int
    generator: Tuple[int, int] # (x, y)

    @property
    def identity(self) -> 'Point':
        return Point(0, 0, curve=self)

    # Generate a point on the curve by multiplying the generator point by a given scalar k
    def generate_point(self, k: int) -> 'Point':
        return Point(*self.generator, curve=self) * k

    # `(a, b) in curve` returns whether the given point is on the curve
    def __contains__(self, point: 'Point') -> bool:
        # Special case: the point at infinity is on the curve
        if point.is_identity():
            return True
        
        x, y = point.x, point.y
        return pow(y, 2, self.p) == (pow(x, 3, self.p) + self.a * x + self.b) % self.p


@dataclass(frozen=True)
class Point:
    x: int
    y: int
    curve: EllipticCurve

    def is_identity(self) -> bool:
        return self.x == 0 and self.y == 0
    
    # Perturb the point to something that's not on the curve; this is useful for testing
    def perturb(self, delta_x: int, delta_y: int) -> 'Point':
        return Point(self.x + delta_x, self.y + delta_y, self.curve)

    def __add__(self, other: 'Point') -> 'Point':
        if self.is_identity():
            return other
        if other.is_identity():
            return self
        
        # Note that duplicate curves with identical parameters are NOT considered
        # equivalent for the purposes of group operations; this may prevent subtle bugs
        # and ensures that this check can be a fast pointer comparison
        curve = self.curve
        assert curve is other.curve, "Points must be on the same curve to add them"

        x1, y1 = self.x, self.y
        x2, y2 = other.x, other.y

        # See https://www.youtube.com/watch?v=vnpZXJL6QCQ&t=3292s
        rise = (y2 - y1) % curve.p
        run = (x2 - x1) % curve.p

        # Singularities in the slope formula occur when points are either identical or
        # are mirror images of each other about the x-axis
        if run == 0:
            # Points are mirror images; return the point at infinity
            if rise != 0:
                return curve.identity
            
            # Points are identical; use the tangent line at the point
            else:
                slope = (3 * pow(x1, 2, curve.p) + curve.a) * pow(2 * y1, -1, curve.p)
        else:
            run_inv = pow(run, -1, curve.p)
            slope = (rise * run_inv) % curve.p

        x3 = (pow(slope, 2, curve.p) - x1 - x2) % curve.p
        y3 = (slope * (x1 - x3) - y1) % curve.p

        return Point(x3, y3, curve)
    
    # Recursive double-and-add algorithm, adapted from https://en.wikipedia.org/wiki/Exponentiation_by_squaring
    def __mul__(self, scalar: int) -> 'Point':
        if scalar < 0:
            return -self * -scalar
        
        if scalar == 0:
            return self.curve.identity
        
        if scalar == 1:
            return self
        
        if scalar % 2 == 0:
            return (self + self) * (scalar // 2)
        
        # Odd scalar > 1
        return (self + self) * ((scalar - 1) // 2)
    
    # Allow either k * point or point * k
    def __rmul__(self, scalar: int) -> 'Point':
        return self * scalar

    # Negation is reflection about the x-axis
    def __neg__(self) -> 'Point':
        curve = self.curve
        return Point(self.x, -self.y % curve.p, curve)


# Standard NIST curves
NIST_P192 = EllipticCurve(
    a=-3,
    b=2455155546008943817740293915197451784769108058161191238065,
    p=6277101735386680763835789423207666416083908700390324961279,
    generator=(602046282375688656758213480587526111916698976636884684818, 174050332293622031404857552280219410364023488927386650641)
)

NIST_P224 = EllipticCurve(
    a=-3,
    b=18958286285566608000408668544493926415504680968679321075787234672564,
    p=26959946667150639794667015087019630673557916260026308143510066298881,
    generator=(
        19277929113566293071110308034699488026831934219452440156649784352033,
        19926808758034470970197974370888749184205991990603949537637343198772
    )
)

NIST_P256 = EllipticCurve(
    a=-3,
    b=41058363725152142129326129780047268409114441015993725554835256314039467401291,
    p=115792089210356248762697446949407573530086143415290314195533631308867097853951,
    generator=(
        48439561293906451759052585252797914202762949526041747995844080717082404635286,
        36134250956749795798585127919587881956611106672985015071877198253568414405109
    )
)

NIST_CURVES = (NIST_P192, NIST_P224, NIST_P256)
