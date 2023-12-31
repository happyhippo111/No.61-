from ECDSA import * 
import random
import string
n=19
a = 2
b = 2
G = [7, 1]
k = 2
message = "Im Satoshi"
# print(Point_Add([5,1],G))
# print(Multi(k,G))
d = 5
r, s = ECDSA_Sign(message, G, d, k,n)
P = Multi(d, G)
print("公钥为", P)
print("根据私钥签名为：（",r,"，",s,"）")
# print((r,s))
print("验证使用私钥的签名……")
ECDSA_Verify(message, G, r, s, P,n)

print("///////////////////////////////////////////////////////////////////////")
print("在未知私钥的前提下开始伪造签名……")
u=random.randint(1,n-1)
v=random.randint(1,n-1)
R=Point_Add(Multi(u, G),Multi(v, P))
r=R[0]
s=(r*Multi_inverse(v,n))%n
e=(u*s)%n   #e=H(m)

print("伪造的签名为：（",r,"，",s,"）")#签名结果为（r,s）
print("验证伪造的签名……")
ECDSA_Verify_e(e, G, r, s, P,n)
