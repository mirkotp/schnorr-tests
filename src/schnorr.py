from charm.toolbox.ecgroup import ECGroup, ZR
from charm.toolbox.eccurve import secp256k1
from charm.core.math.elliptic_curve import getGenerator

# Setup group
G = ECGroup(secp256k1)
g = getGenerator(G.ec_group)

# Schnorr signature implementation
def sign(x, m):
    r = G.random(ZR)
    R = g ** r
    c = G.hash((R, m))
    s = x * c + r
    return (R, s)

def verify(X, m, sig):
    R, s = sig
    c = G.hash((R, m))
    return g ** s == R * X ** c

# Generate private/public key pair
x = G.random(ZR)
X = g ** x

# Signed message
m = "Hi, how are you?"

# Sign
sig = sign(x, m)

# Verify
assert(verify(X, m, sig))
print("Valid signature")