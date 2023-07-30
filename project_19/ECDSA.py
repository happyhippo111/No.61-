import hashlib

'''
设待签名的消息为M，为了获取消息M的数字签名(r,s)，作为签名者的用户A应实现以下运算步
骤：
A1：置M=ZA ∥ M；
A2：计算e = Hv(M)，按本文本第1部分4.2.3和4.2.2给出的细节将e的数据类型转换为整数；
A3：用随机数发生器产生随机数k ∈[1,n-1]；
A4：计算椭圆曲线点(x1,y1)=[k]G，按本文本第1部分4.2.7给出的细节将x1的数据类型转换为整
数；
A5：计算r=(e+x1) modn，若r=0或r+k=n则返回A3；
A6：计算s = ((1 + dA)
−1
· (k − r · dA)) modn，若s=0则返回A3；
A7：按本文本第1部分4.2.1给出的细节将r、s的数据类型转换为字节串，消息M 的签名为(r,s)
'''


# 辗转相除法求最大公约数
def get_gcd(a, b):
    re = a % b
    while re != 0:
        a = b
        b = re
        k = a // b
        re = a % b
    return b


# 改进欧几里得算法求线性方程的x与y
def get_(a, b):
    if b == 0:
        return 1, 0
    else:
        k = a // b
        remainder = a % b
        x1, y1 = get_(b, remainder)
        x, y = y1, x1 - k * y1
    return x, y


# 返回乘法逆元
def Multi_inverse(a, b):
    # 将初始b的绝对值进行保存
    if b < 0:
        m = abs(b)
    else:
        m = b

    flag = get_gcd(a, b)
    # 判断最大公约数是否为1，若不是则没有逆元
    if flag == 1:
        x, y = get_(a, b)
        x0 = x % m
        # print(x0) #x0就是所求的逆元
        return x0

    else:
        print("Do not have!")


# 所用的椭圆曲线
# y^2=x^3+ax+by mod (mod_value)

def Point_Add(P, Q):
    if P[0] == Q[0]:
        fenzi = (3 * pow(P[0], 2) + a)
        fenmu = (2 * P[1])
        if fenzi % fenmu != 0:
            val = Multi_inverse(fenmu, 17)
            y = (fenzi * val) % 17
        else:
            y = (fenzi / fenmu) % 17
    else:
        fenzi = (Q[1] - P[1])
        fenmu = (Q[0] - P[0])
        if fenzi % fenmu != 0:
            val = Multi_inverse(fenmu, 17)
            y = (fenzi * val) % 17
        else:
            y = (fenzi / fenmu) % 17

    Rx = (pow(y, 2) - P[0] - Q[0]) % 17
    Ry = (y * (P[0] - Rx) - P[1]) % 17
    return Rx, Ry


def Multi(n, point):
    if n == 0:
        return 0
    elif n == 1:
        return point

    t = point
    while (n >= 2):
        t = Point_Add(t, point)
        n = n - 1
    return t


def double(point):
    return Point_Add(point, point)


def fast_Multi(n, point):
    if n == 0:
        return 0
    elif n == 1:
        return point
    elif n % 2 == 0:
        return Multi(n / 2, double(point))
    else:
        return Point_Add(Multi((n - 1) / 2, double(point)), point)


def ECDSA_Sign(m, G, d, k):
    e = Hash(m)
    R = Multi(k, G)  # R=kg
    # print("R",R)
    r = R[0] % mod_value  # r=R[x] mod mod_value
    s = (Multi_inverse(k, mod_value) * (e + d * r)) % mod_value
    return r, s


def ECDSA_Verify(m, G, r, s, P):
    e = Hash(m)
    w = Multi_inverse(s, mod_value)
    ele1 = (e * w) % mod_value
    ele2 = (r * w) % mod_value
    w = Point_Add(Multi(ele1, G), Multi(ele2, P))
    if w == 0:
        print('false')
        return False
    else:
        if w[0] % mod_value == r:
            print("签名验证通过")
            return True
        else:
            print('签名不通过')
            return False
        
def ECDSA_Verify_e(e, G, r, s, P):
    w = Multi_inverse(s, mod_value)
    ele1 = (e * w) % mod_value
    ele2 = (r * w) % mod_value
    w = Point_Add(Multi(ele1, G), Multi(ele2, P))
    if w == 0:
        print('false')
        return False
    else:
        if w[0] % mod_value == r:
            print("签名验证通过")
            return True
        else:
            print('签名不通过')
            return False

def Hash(string):
    s = hashlib.sha256()
    s.update(string.encode())
    b = s.hexdigest()
    return int(b, 16)


def deduce_pubkey(s, r, k, G):
    ele1 = Multi_inverse((s + r), 17)

    ele2 = Multi(k, G)

    ele3 = Multi(s, G)
    ele4 = (ele3[0], (-ele3[1]) % 17)
    print(ele2, ele4)

    result = Point_Add(ele2, ele4)

    print("根据签名推出公钥", result)


mod_value = 19
a = 2
b = 2
G = [7, 1]
k = 2



