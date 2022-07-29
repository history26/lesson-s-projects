import random,time
V=0x7380166f4914b2b9172442d7da8a0600a96f30bc163138aae38dee4db0fb0e4e
T=[0x79cc4519, 0x7a879d8a]
def inttobin(x,k):#将十进制整型变量转化为k位二进制字符串
    x=bin(x)[2:]
    t=k-len(x)
    while t>0:
        x='0'+x
        t=t-1
    return x

def lshift(x,s):#将a转化为二进制并且左移s位
    x=inttobin(x,32)
    for i in range(s):
        t=x[0]
        x=x[1:]
        x=x+t
    return int(x,2)
def exten(a):#将原消息进行扩展，分成两部分返回，准备压缩
    x=[]
    y=[]
    for i in range(16):
        t=a[32*i:32*(i+1)]
        x.append(int(t,2))
    for j in range(16, 68):
        f1=lshift(x[j-3],15)
        f2=lshift(x[j-13],7)
        t=f1^x[j-9]^x[j-16]
        f3=t^lshift(t,15)^lshift(t, 23)
        f4=f2^f3^x[j-6]
        x.append(f4)
    for j in range(64):
        f=x[j]^x[j+4]
        y.append(f)
    return x,y
def Tj(f):
    if f<=15:
        return T[0]
    else:
        return T[1]

def FF(a,b,c,j):
    if j<=15:
        return a^b^c
    else:
        return (a&b)|(a&c)|(b&c)

def GG(a,b,c,j):
    if j<=15:
        return a^b^c
    else:
        x=inttobin(a,32)
        t=''
        for i in x:
            if i=='0':
                t=t+'1'
            else:
                t=t+'0'
        return (a&b)|((int(t,2))&c)


def CF(a, w, w1):#压缩函数，将扩展得到的消息迭代压缩
    x = []
    for i in range(8):
        t=a[32*i:32*(i+1)]
        x.append(int(t,2))
    for j in range(64):
        SS1 = lshift((lshift(x[0],12) +x[4]+ lshift(Tj(j),j%32))% 2**32,7)
        SS2 = SS1 ^ lshift(x[0], 12)
        TT1 = (FF(x[0],x[1],x[2],j)+x[3]+SS2+w1[j])% 2**32
        TT2 = (GG(x[4],x[5],x[6],j)+x[7]+SS1+w[j])% 2**32
        x[7]=x[6]
        x[6]=lshift(x[5], 19)
        x[5]=x[4]
        x[4]=TT2^lshift(TT2, 9)^lshift(TT2, 17)
        x[3]=x[2]
        x[2]=lshift(x[1], 9)
        x[1]=x[0]
        x[0]=TT1
    t = inttobin(x[0],32)+inttobin(x[1],32)+inttobin(x[2],32)+inttobin(x[3],32)+inttobin(x[4],32)+inttobin(x[5],32)+inttobin(x[6],32)+inttobin(x[7],32)
    res = int(t,2)
    return int(a,2)^res

def extance(m):#将消息按照规则扩展到长度为512的整数倍
    m=bin(m)[2:]
    while len(m)%4 !=0:
        m='0'+m
    k=448-(len(m)+1) % 512
    if (k < 0):  
        k=k+512
    m=m+'1'+'0'*k+inttobin(len(m), 64)
    return m

def roundfunc(p):#实现压缩过程的轮函数
    n=int(len(p)/512)
    r=[]
    r.append(inttobin(V,256))
    for i in range(n):
        w,w1 = exten(p[512*i:512*(i+1)])
        t=CF(r[i],w, w1)
        res=inttobin(t,256)
        r.append(res)
    return r[n]
def sm3(m):#输入为整数，输出为二进制字符串
    m1=extance(m)
    res=roundfunc(m1)
    return res

def attack(n):#生日攻击的过程，由于计算力，只研究前n位的碰撞
    for i in range(2**n):
        ps = random.sample(range(0,2**n),2**(n//2))
        for j in range(len(ps)-1):
            for k in range(j+1,len(ps)):
                if sm3(ps[j])[:n]==sm3(ps[k])[:n]:
                    print('攻击成功：两个输入为',bin(ps[j])[2:],'和',bin(ps[k])[2:],'时')
                    print('得到的哈希结果为')
                    print(sm3(ps[j]))
                    print('和')
                    print(sm3(ps[k]))
                    print('它们的前',n,'位相等')
                    return
    print('攻击失败')

start = time.time()
attack(8)#通过调整这里的数字来根据sm3结果的对前n位是否相同进行攻击
end = time.time()
print('攻击用时', end-start, 's')


