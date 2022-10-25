from ..pair import Pair
from ..utils import unpack
from ..cipher import stream
from ..cipher.sm2 import SM2, SM2_Point

def recv(pair: Pair, b: int) -> bytes:
    assert b == 0 or b == 1, "b should be 0 or 1"

    sm2 = SM2()
    
    ak = pair.recv()
    ak = sm2.bytes_to_point(ak)
    pk = sm2.pk
    
    # choose point and pk
    if b == 1:
        pk = SM2_Point(sm2.pk) + SM2_Point(ak)
        pk = pk.xy
    # send chosen public key
    pair.send(sm2.point_to_bytes(pk))

    ck = sm2.sk * SM2_Point(ak)
    # receive cipher msg
    cipher_m = unpack(pair.recv())[b]

    res = stream.decrypt(sm2.point_to_bytes(ck.xy), cipher_m)
    
    return res
