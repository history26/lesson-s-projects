import random,math,SM2,SM3
from gmpy2 import invert
#预处理
def f1(a,b,Gx,Gy,Px,Py,p):
    ENTL='00010000'
    ID='31323334353637383132333435363738'
    ID=SM2.msg2bit(ID)
    a=SM2.Fq2bit(a,p)
    b=SM2.Fq2bit(b,p)
    Gx=SM2.point2bit(Gx,Gy,p)
    Px=SM2.point2bit(Px,Py,p)
    Z=SM3.SM3_digest(ENTL+ID+a+b+Gx+Px)
    return Z
def f2(Z,M):
    return SM3.SM3_digest(Z+M)
#签名
def signfuc(d,z,H,msg,n,a,b,Gx,Gy,Px,Py,p):
    #1
    M1=z+H
    #2
    e=SM3.SM3_digest(M1)
    e=SM2.bit2Fq(e)
    #3
    k=random.randint(1,n-1)
    #4
    x1, y1 = SM2.multiplyk_point(Gx, Gy, k, a, p)
    #5
    r=(e+x1)%n
    if r==0:
        return False
    if r+k==n:
        return False
    #6

    s=(invert(1+d,n)*(k-r*d))%n
    s=int(s)
    if s==0:
        return False
    r=SM2.Fq2bit(r,p)
    s=SM2.Fq2bit(s,p)
    return r,s


#验证
def verify(r,s,z,H,n,a,b,Gx,Gy,Px,Py):
    r=SM2.bit2Fq(r)
    s=SM2.bit2Fq(s)
    #1
    if r<1 or r>n-1:
        print("不通过")
        return False
    #2
    if s<1 or s>n-1:
        print("不通过-s")
        return False
    #3
    M2=z+H
    #4
    e=SM3.SM3_digest(M2)
    e=SM2.bit2Fq(e)
    #5
    t=(r+s)%n
    if t==0:
        print("不通过-t")
        return False
    #6
    x1,y1=SM2.multiplyk_point(Gx, Gy, s, a, p)
    x2,y2=SM2.multiplyk_point(Px, Py, t, a, p)
    x1,x2=SM2.add_point(x1,y1,x2,y2,p)
    #7
    R=(e+x1)%n
    if R==r:
        print("验证成功")
        return True
    else:
        print("不通过-r")
        return False
    
    

p = int('FFFFFFFEFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF00000000FFFFFFFFFFFFFFFF', base=16)
a = int('FFFFFFFEFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF00000000FFFFFFFFFFFFFFFC', base=16)
b = int('28E9FA9E9D9F5E344D5A9E4BCF6509A7F39789F515AB8F92DDBCBD414D940E93', base=16)
n = int('FFFFFFFEFFFFFFFFFFFFFFFFFFFFFFFF7203DF6B21C6052B53BBF40939D54123', base=16)
Gx = int('32C4AE2C1F1981195F9904466A39C9948FE30BBFF2660BE1715A4589334C74C7', base=16)
Gy = int('BC3736A2F4F6779C59BDCEE36B692153D0A9877CC62A474002DF32E52139F0A0', base=16)

d, Px, Py = SM2.gen_keypair(n, Gx, Gy, a, b, p)

msg="sample"
z=f1(a,b,Gx,Gy,Px,Py,p)
H=f2(z,msg)
r_q,s_q=signfuc(d,z,H,msg,n,a,b,Gx,Gy,Px,Py,p)
print("消息M为",msg)
print("加密后的密文为",hex(int(H,2)))
print("签名为r",hex(int(r_q,2)))
print("签名为s",hex(int(s_q,2)))
verify(r_q,s_q,z,H,n,a,b,Gx,Gy,Px,Py)
