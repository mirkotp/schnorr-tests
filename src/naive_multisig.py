from charm.toolbox.ecgroup import ECGroup, ZR
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
r = [group.random(ZR) for _ in range(N)]
R = [g ** r_i for r_i in r]

R_tot = reduce(mul, R)
X = reduce(mul, pk)
c = group.hash((X, R_tot, m))

s = [r[i] + c * sk[i] for i in range(N)]
s_tot = reduce(add, s)
signature = (R_tot, s_tot)

# Verify
X = reduce(mul, pk)
(R, s) = signature
c = group.hash((X, R, m))

assert(g ** s == R * X ** c)
print("Valid signature")