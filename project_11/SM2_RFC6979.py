from Crypto.Util.number import inverse
import hashlib
import hmac
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
    slope = (3 * p[0] ** 2 + A) *inverse(2 * p[1], P) % P

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

def rfc6979_generate_k(hash_func, private_key, message, curve_order):
    """
    根据RFC 6979生成ECDSA签名的确定性k值。

    参数：
        hash_func (callable)：用于计算消息摘要的哈希函数。
        private_key (int)：用于签名的私钥。
        message (bytes)：要签名的消息。
        curve_order (int)：ECDSA中使用的椭圆曲线的阶。

    返回：
        int：用于ECDSA签名的确定性k值。
    """

    def bits2int(bits):
        return int.from_bytes(bits, 'big')

    def int2octets(x):
        return x.to_bytes((x.bit_length() + 7) // 8, 'big')

    # 步骤1：计算私钥和消息的哈希。
    h1 = hash_func(int2octets(private_key) + message).digest()

    # 步骤2：初始化变量。
    V = b'\x01' * 32
    K = b'\x00' * 32
    K = hmac.new(K, V + b'\x00' + h1, hash_func).digest()
    V = hmac.new(K, V, hash_func).digest()
    K = hmac.new(K, V + b'\x01' + h1, hash_func).digest()
    V = hmac.new(K, V, hash_func).digest()

    # 步骤3：主循环计算K
    while True:
        T = b''
        while len(T) < 32:
            V = hmac.new(K, V, hash_func).digest()
            T += V
        k = bits2int(T)
        if k >= 1 and k < curve_order:
            return k

        K = hmac.new(K, V + b'\x00', hash_func).digest()
        V = hmac.new(K, V, hash_func).digest()


def sm2_sign(private_key, message):
    # 步骤1：已在你的代码中定义椭圆曲线参数和基点G
    # 步骤2：生成随机整数k，你可以使用RFC 6979算法或其他随机数生成器
    k = rfc6979_generate_k(hashlib.sha256, private_key, message, N)
    # 步骤3：计算椭圆曲线点S = k * G
    S = ECC_mul(k, G)
    
    Z = hashlib.sha256(message).digest()
    # 步骤5：计算e = Z mod N
    e = int.from_bytes(Z, 'big') % N
    # 步骤6：计算k的逆元k_inv = Multi_inverse(k, N)
    k_inv = Multi_inverse(k, N)
    # 步骤7：计算签名参数r = (e + S_X) mod N
    r = (e + S[0]) % N
    # 步骤8：计算((1+d)^-1* (k - r * private_key)) mod N，其中s_inv为s的逆元
    s_inv = Multi_inverse(1+prikey, N)
    s = (s_inv * (k - r * private_key)) % N

    # 步骤9：返回签名(r, s)
    return r, s
def sm2_Verify(r,s, message, public_key):
    # 计算消息的哈希值Z = Hash(message)
    Z = hashlib.sha256(message).digest()
    # 计算e = Z mod N
    e = int.from_bytes(Z, 'big') % N
    #
    t=(r+s)%N
    x,y=Point_Add(ECC_mul(s, G), ECC_mul(t, public_key))
    R=(e+x)%N
    if(R==r):
        print("签名验证终于成功啦！！")
    else:
        print("很好，你需要继续debug了")
        
prikey = 0x5f6717883bef25f45a129c11fcac1567d74bda5a9ad4cbffc8203c0da2a1473c
pubkey = ECC_mul(prikey, G)
message = b"Hello, world!"
r,s=sm2_sign(prikey, message)
print("对消息签名中……")
print("签名为:(",r,",",s,")")
print("对签名验证中……")
sm2_Verify(r,s, message,pubkey)
