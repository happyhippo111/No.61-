import hashlib

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


def ECDSA_Sign(m, G, d, k,n):
    e = Hash(m)
    R = Multi(k, G)  # R=kg
    # print("R",R)
    r = R[0] % n  # r=R[x] mod mod_value
    s = (Multi_inverse(k, n) * (e + d * r)) % n
    return r, s


def ECDSA_Verify(m, G, r, s, P,n):
    e = Hash(m)
    w = Multi_inverse(s, n)
    ele1 = (e * w) % n
    ele2 = (r * w) % n
    w = Point_Add(Multi(ele1, G), Multi(ele2, P))
    if w == 0:
        print('false')
        return False
    else:
        if w[0] % n == r:
            print("签名验证通过")
            return True
        else:
            print('签名不通过')
            return False
        
def ECDSA_Verify_e(e, G, r, s, P,n):
    w = Multi_inverse(s, n)
    ele1 = (e * w) % n
    ele2 = (r * w) % n
    w = Point_Add(Multi(ele1, G), Multi(ele2, P))
    if w == 0:
        print('false')
        return False
    else:
        if w[0] % n == r:
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


def deduce_pubkey(s, r, k, G,n):
    ele1 = Multi_inverse((s + r), n)

    ele2 = Multi(k, G)

    ele3 = Multi(s, G)
    ele4 = (ele3[0], (-ele3[1]) % n)
    #print(ele2, ele4)

    result = Point_Add(ele2, ele4)

    print("根据签名推出公钥", result)
# 椭圆曲线 E17(2,2)
n=19
a = 2
b = 2
G = [7, 1]
k = 2



