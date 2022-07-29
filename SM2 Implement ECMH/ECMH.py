import random,math
from gmssl import sm3, func
# 模运算
def mod(a, b):  
    if math.isinf(a):
        return float('inf')
    else:
        return a % b
#计算x=(n*d^(-1))%b
def mod_decimal(n, d, b):  
    if d == 0:
        x = float('inf')
    elif n == 0:
        x = 0
    else:
        a = bin(b - 2).replace('0b', '')
        y = 1
        i = 0
        while i < len(a):  
            y = (y ** 2) % b  
            if a[i] == '1':
                y = (y * d) % b
            i += 1
        x = (y * n) % b
    return x
#计算二次剩余
def Legendre(n, p):  
    return pow(n, (p - 1) // 2, p)
# Tonelli-Shanks算法求二次剩余
def T_S(n, p):  
    assert Legendre(n, p) == 1#判断二次剩余
    if p % 4 == 3:
        return pow(n, (p + 1) // 4, p)
    q = p - 1
    s = 0
    while q % 2 == 0:
        q = q // 2
        s += 1
    for z in range(2, p):
        if Legendre(z, p) == p - 1:
            c = pow(z, q, p)
            break
    r = pow(n, (q + 1) // 2, p)
    t = pow(n, q, p)
    m = s
    if t % p == 1:
        return r
    else:
        i = 0
        while t % p != 1:
            temp = pow(t, 2 ** (i + 1), p)
            i += 1
            if temp % p == 1:
                b = pow(c, 2 ** (m - i - 1), p)
                r = r * b % p
                c = b * b % p
                t = t * c % p
                m = i
                i = 0
        return r

#椭圆曲线点加
def add_point(Px,Py, Qx,Qy, a, p):  
    if (math.isinf(Px) or math.isinf(Py)) and (~math.isinf(Qx) and ~math.isinf(Qy)): 
        Rx = Qx
        Ry=Qy
    elif (~math.isinf(Px) and ~math.isinf(Py)) and (math.isinf(Qx) or math.isinf(Qy)):  
        Rx = Px
        Ry=Qy
    elif (math.isinf(Px) or math.isinf(Py)) and (math.isinf(Qx) or math.isinf(Qy)): 
        Rx = float('inf')
        Ry = float('inf')
    else:
        if Px != Qx or Py != Qy:
            l = mod_decimal(Qy - Py, Qx - Px, p)
        else:
            l = mod_decimal(3 * Px ** 2 + a, 2 * Py, p)
        x = mod(l ** 2 - Px - Qx, p)
        y = mod(l * (Px - x) - Py, p)
        Rx= x
        Ry= y
    return Rx,Ry

#椭圆曲线点乘
def mul_point(k, Px,Py, a, p):  
    k_b = bin(k).replace('0b', '')  
    i = len(k_b) - 1
    Rx = Px
    Ry=Py
    if i > 0:
        k = k - 2 ** i
        while i > 0:
            Rx,Py = add_point(Rx,Ry, Rx,Ry, a, p)
            i -= 1
        if k > 0:
            x,y=mul_point(k, Px,Py, a, p)
            Rx,Ry = add_point(Rx,Ry, x,y, a, p)
    return Rx,Ry
#公私钥生成算法
def key_gen(a, p, n, Gx,Gy):  

    d = random.randint(1, n - 2)
    Px,Py = mul_point(d, Gx,Gy, a, p)
    return d,Px,Py
#哈希
def SetHash(setting):  # 
    x1 = float("inf")
    y1=float("inf")
    for i in setting:
        x = int(sm3.sm3_hash(func.bytes_to_list(i)), 16)
        temp = mod(x ** 2 + a * x + b, p)
        y = T_S(temp, p)
        x2,y2 = add_point(x1,y1, x, y, a, p)
    return x2,y2
#实例运行
if __name__ == '__main__':
    p = 0xFFFFFFFEFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF00000000FFFFFFFFFFFFFFFF
    a = 0xFFFFFFFEFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF00000000FFFFFFFFFFFFFFFC
    b = 0x28E9FA9E9D9F5E344D5A9E4BCF6509A7F39789F515AB8F92DDBCBD414D940E93
    n = 0xFFFFFFFEFFFFFFFFFFFFFFFFFFFFFFFF7203DF6B21C6052B53BBF40939D54123
    Gx = 0x32C4AE2C1F1981195F9904466A39C9948FE30BBFF2660BE1715A4589334C74C7
    Gy = 0xBC3736A2F4F6779C59BDCEE36B692153D0A9877CC62A474002DF32E52139F0A0
    d,Px,Py = key_gen(a, p, n, Gx,Gy)
    print("私钥",d)
    print("公钥")
    print(Px)
    print(Py)
    set1 = (b'1234',b'12345')
    x_1,y_1 = SetHash(set1)
    print("hash_1 ", "\n",x_1,"\n",y_1)
    set2 = (b'1234', )
    x_2,y_2= SetHash(set2)
    print("hash_2  ","\n" ,x_2,"\n",y_2)
