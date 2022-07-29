import random,math,SM2,SM3
from gmpy2 import invert

ID_A='31323334353637383132333435363738'
ID_B='11323334353637383132333435363738'
p=int('0x8542D69E4C044F18E8B92435BF6FF7DE457283915C45517D722EDB8B08F1DFC3',base=16)   
a=int('0x787968B4FA32C3FD2417842E73BBFEFF2F3C848B6831D7E0EC65228B3937E498',base=16) 
b=int('0x63E4C6D3B23B0C849CF84241484BFE48F61D59A5B16BA06E6E12D1DA27C5249A',base=16) 
n=int('0x8542D69E4C044F18E8B92435BF6FF7DD297720630485628D5AE74EE7C32E79B7',base=16) 
Gx=int('0x421DEBD61B62EAB6746434EBC3CC315E32220B3BADD50BDC4C4E6C147FEDD43D',base=16) 
Gy=int('0x0680512BCBB42C07D47349D2153B70C4E5D7FDFCBFA36EA1A85841B9E46E09A2',base=16) 
klen=128
da, Px_a, Py_a = SM2.gen_keypair(n, Gx, Gy, a, b, p)
db, Px_b, Py_b = SM2.gen_keypair(n, Gx, Gy, a, b, p)
#预处理
w=math.ceil(math.ceil(math.log2(n))/2)-1
h=1
def f1(a,b,Gx,Gy,Px,Py,p,ID):
    ENTL='00010000'
    ID=SM2.msg2bit(ID)
    a=SM2.Fq2bit(a,p)
    b=SM2.Fq2bit(b,p)
    Gx=SM2.point2bit(Gx,Gy,p)
    Px=SM2.point2bit(Px,Py,p)
    Z=SM3.SM3_digest(ENTL+ID+a+b+Gx+Px)
    return Z
ZA=f1(a,b,Gx,Gy,Px_a,Py_a,p,ID_A)
ZB=f1(a,b,Gx,Gy,Px_b,Py_b,p,ID_B)



ra=random.randint(1,n-1)
xA,yA=SM2.multiplyk_point(Gx, Gy, ra, a, p)


def ex_B(xA,yA):
    rb=random.randint(1,n-1)
    xB,yB=SM2.multiplyk_point(Gx, Gy, rb, a, p)
    x2=2**w+(xB&((2**w)-1))
    tb=(db+x2*rb)%n
    x1=2**w+(xA&((2**w)-1))
    xV,yV=SM2.multiplyk_point(xA, yA, x1, a, p)
    xV,yV=SM2.add_point(xV,yV,Px_a,Py_a,p)
    xV,yV=SM2.multiplyk_point(xV, yV, h*tb, a, p)
    xV_bit=SM2.Fq2bit(xV, p)
    yV_bit=SM2.Fq2bit(yV, p)
    Kb=SM2.KDF(xV_bit+yV_bit+ZA+ZB,klen)
    print("Kb",int(Kb,2))
    xA_bit=SM2.Fq2bit(xA, p)
    yA_bit=SM2.Fq2bit(yA, p)
    xB_bit=SM2.Fq2bit(xB, p)
    yB_bit=SM2.Fq2bit(yB, p)
    Sb=SM3.SM3_digest(xV_bit+ZA+ZB+xA_bit+yA_bit+xB_bit+yB_bit)
    Sb=SM3.SM3_digest("0x02"+yV_bit+Sb)
    return rb,xB,yB,Sb,xV_bit,yV_bit
def ex_A(ra,xA,yA,xB,yB,Sb):
    
    x1=2**w+(xA&((2**w)-1))
    ta=(da+x1*ra)%n
    x2=2**w+(xB&((2**w)-1))
    xU,yU=SM2.multiplyk_point(xB, yB, x2, a, p)
    xU,yU=SM2.add_point(xU,yU,Px_b,Py_b,p)
    xU,yU=SM2.multiplyk_point(xU, yU, h*ta, a, p)
    xU_bit=SM2.Fq2bit(xU, p)
    yU_bit=SM2.Fq2bit(yU, p)
    xA_bit=SM2.Fq2bit(xA, p)
    yA_bit=SM2.Fq2bit(yA, p)
    xB_bit=SM2.Fq2bit(xB, p)
    yB_bit=SM2.Fq2bit(yB, p)
    S1=SM3.SM3_digest(xU_bit+ZA+ZB+xA_bit+yA_bit+xB_bit+yB_bit)
    S1=SM3.SM3_digest("0x02"+yU_bit+S1)
    if S1!=Sb:
        print("S1")
        return False
    Ka=SM2.KDF(xU_bit+yU_bit+ZA+ZB,klen)
    print("Ka",int(Ka,2))
    Sa=SM3.SM3_digest(xU_bit+ZA+ZB+xA_bit+yA_bit+xB_bit+yB_bit)
    Sa=SM3.SM3_digest("0x03"+yU_bit+Sa)
    return Sa

def ver_b(Sa,xV_bit,yV_bit):
    xA_bit=SM2.Fq2bit(xA, p)
    yA_bit=SM2.Fq2bit(yA, p)
    xB_bit=SM2.Fq2bit(xB, p)
    yB_bit=SM2.Fq2bit(yB, p)
    S2=SM3.SM3_digest(xV_bit+ZA+ZB+xA_bit+yA_bit+xB_bit+yB_bit)
    S2=SM3.SM3_digest("0x03"+yV_bit+S2)
    if S2==Sa:
        print("交换成功")
        return True
    else:
        print("交换失败")
    return False

   
#print("ra ",ra)
rb,xB,yB,Sb,xV_bit,yV_bit=ex_B(xA,yA)
#print("rb ",rb)
Sa=ex_A(ra,xA,yA,xB,yB,Sb)
ver_b(Sa,xV_bit,yV_bit)


    
    
    
    
