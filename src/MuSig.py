from charm.toolbox.ecgroup import ECGroup, ZR, G
from charm.toolbox.eccurve import secp256k1 as curve
from charm.core.math.elliptic_curve import getGenerator
from functools import reduce
from operator import add, mul

# Setup
N = 10
m = "Hi, how are you?"
group = ECGroup(curve)
g = getGenerator(group.ec_group)
sk = [group.random(ZR) for _ in range(N)]
pk = [g ** k_i for k_i in sk]

# Sign
a = [group.hash((*pk, k_i)) for k_i in pk]
X = reduce(mul, [pk_i ** a_i for (pk_i, a_i) in zip(pk, a)])
r = [group.random(ZR) for _ in range(N)]
R = [g ** r_i for r_i in r]
# At this point all parties should receive commitments
# for the various R[i] before exposing their own R,
# but we skip this part.

R_tot = reduce(mul, R)
c = group.hash((X, R_tot, m))

s = [r[i] + c * a[i] * sk[i] for i in range(N)]
s_tot = reduce(add, s)
signature = (R_tot, s_tot)

# Verify
a = [group.hash((*pk, k_i)) for k_i in pk]
(R, s) = signature
X = reduce(mul, [pk_i ** a_i for (pk_i, a_i) in zip(pk, a)])
c = group.hash((X, R_tot, m))

assert(g ** s == R * X ** c)
print("Valid signature")