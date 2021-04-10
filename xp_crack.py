import hashlib
import random
import numpy
from sage.all import *


def left_to_right_double_and_add(n, G):
    """n is a positive integer number,
    G is a rational point of an elliptic curve E, 
    defined over some finite field F.
    This routine computes
    n*G
    in an ad-hoc manner.
    We use the standard add, and doubling on E,
    and do not implemented them here.
    """
    digits = ZZ(n).digits(base=2)
    E = G.curve()
    # F = E.base_field()
    P = G    # this corresponds to 1*G, init
    nG = E(0)    # and we add further contributions
    for digit in digits:
        if digit:
            nG = nG.__add__(P)    # or simply nG += P
        P = P.__mul__(2)          # or simply P  *= 2
        # print "\tdigit=%s P=%s nG=%s" % (digit, P, nG)
    return nG



def mod(num, a):
     
    # Initialize result
    res = 0
 
    # One by one process all digits
    # of 'num'
    for i in range(0, len(num)):
        res = (res * 10 + int(num[i])) % a;
 
    return res



def generate_valid_key():
    import random
    alphabet_encoding = "BCDFGHJKMPQRTVWXY2346789"
    pid = 640000000 << 1
    p = 0x92ddcf14cb9e71f4489a2e9ba350ae29454d98cb93bdbcc07d62b502ea12238ee904a8b20d017197aae0c103b32713a9
    priv = 0x565b0dff8496c8
    order = 0xdb6b4c58efbafd
    a = 0x1
    b = 0x0
    key = 0x0
    r = 0x0 
    s = 0x0 
    h = 0x0 
    rez = 0x0
    maxKey = pow(24,25) - 1
    E = EllipticCurve(GF(p), [a, b])
    g = E.gen(0)

    while(key < maxKey):
        r =  random.getrandbits(7) # when refacotring this becomes k
        rez = left_to_right_double_and_add(r,g)
        h = hashlib.sha1((
                chr(pid & 0xff) +
                chr((pid >> 8) & 0xff) +
                chr((pid >> 16) & 0xff) +
                chr((pid >> 24) & 0xff) +
                str(rez[0]) + str(rez[1])).encode('utf-8')
            )

        h = h.hexdigest()[0:8]
        h = ( ord(h[0]) + ord(h[1]) << 8 + ord(h[2]) << 16 + ord(h[3]) << 24) >> 4
        s = h * priv
        s = mod(str(s),order)
        s = r + s
        while(s >= order ):
            s -= order
        key = int(hex(pid),16)
        key += (h << 31)
        key += (s << 59)
    skey = ""
    
    for i in range(25): 
        t = (divmod(key,24))
        key = t[0]  
        t = t[1]
        #print(alphabet_encoding[t])
        skey += alphabet_encoding[t]
    

    final = ""
    for i in range(25):
        final += skey[i]
        if((i != 24) and (i % 5 == 4)):
            final += "-"
    print(final)
    


for i in range(10):
    generate_valid_key()