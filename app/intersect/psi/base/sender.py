from ..pair import Pair
from ..utils import pack
from ..cipher import stream
from ..cipher.sm2 import SM2, SM2_Point

def send(pair: Pair, m0: bytes, m1: bytes, curve: str = "secp256r1"):
    sm2 = SM2()
    
    pk_bytes = sm2.point_to_bytes(sm2.pk)
    pair.send(pk_bytes)

    bk = pair.recv()
    bk = sm2.bytes_to_point(bk)

    # cipher key for m0 and m1
    ck0 = sm2.sk * SM2_Point(bk)
    ck1 = (-SM2_Point(sm2.pk) + SM2_Point(bk)) * sm2.sk
    
    cipher_m0 = stream.encrypt(sm2.point_to_bytes(ck0.xy), m0)
    cipher_m1 = stream.encrypt(sm2.point_to_bytes(ck1.xy), m1)

    pair.send(pack(cipher_m0, cipher_m1))
    


    
    
