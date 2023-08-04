from Crypto.Util.number import inverse
from gmssl import sm3

# 常量定义
P = 0xFFFFFFFEFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF00000000FFFFFFFFFFFFFFFF
N = 0xFFFFFFFEFFFFFFFFFFFFFFFFFFFFFFFF7203DF6B21C6052B53BBF40939D54123
A = 0xFFFFFFFEFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF00000000FFFFFFFFFFFFFFFC
B = 0x28E9FA9E9D9F5E344D5A9E4BCF6509A7F39789F515AB8F92DDBCBD414D940E93
G_X = 0x32C4AE2C1F1981195F9904466A39C9948FE30BBFF2660BE1715A4589334C74C7
G_Y = 0xBC3736A2F4F6779C59BDCEE36B692153D0A9877CC62A474002DF32E52139F0A0
G = (G_X, G_Y)


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


# 椭圆曲线点加法运算
def Point_Add(a, b):
    if a == 0 and b == 0:
        return 0
    elif a == 0:
        return b
    elif b == 0:
        return a
    else:
        if a[0] > b[0]:
            a, b = b, a
        slope = (b[1] - a[1]) * inverse(b[0] - a[0], P) % P

        r = [(slope ** 2 - a[0] - b[0]) % P]
        r.append((slope * (a[0] - r[0]) - a[1]) % P)

        return (r[0], r[1])


def ECC_double(p):
    slope = (3 * p[0] ** 2 + A) * inverse(2 * p[1], P) % P

    r = [(slope ** 2 - 2 * p[0]) % P]
    r.append((slope * (p[0] - r[0]) - p[1]) % P)

    return (r[0], r[1])


def ECC_mul(s, p):
    n = p
    r = 0
    s_binary = bin(s)[2:]
    s_length = len(s_binary)
    for i in reversed(range(s_length)):
        if s_binary[i] == '1':
            r = Point_Add(r, n)
        n = ECC_double(n)

    return r

def KDF(Z, klen):
    hlen = 256
    n = (klen // hlen) + 1
    if n >= 2 ** 32 - 1:
        raise ValueError("The hash length is too large!")
    K = ''
    for i in range(n):
        ct = (hex(i + 1)[2:]).rjust(32, '0')
        tmp_b = bytes.fromhex(Z + ct)
        Kct = sm3.sm3_hash(list(tmp_b))
        K += Kct
    bit_len = 256 * n
    K = (bin(int(K, 16))[2:]).rjust(bit_len, '0')
    K = K[:klen]
    return K
