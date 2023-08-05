from SM2_RFC6979 import *
def sm2_sign_leaking_k(private_key, message):
    k = rfc6979_generate_k(hashlib.sha256, private_key, message, N)
    S = ECC_mul(k, G)
    Z = hashlib.sha256(message).digest()
    e = int.from_bytes(Z, 'big') % N
    k_inv = Multi_inverse(k, N)
    r = (e + S[0]) % N
    s_inv = Multi_inverse(1+private_key, N)
    s = (s_inv * (k - r * private_key)) % N
    return r, s,k

def leaking_k_gen_prikey(r,s,k):
    private_key=(Multi_inverse((s+ r), N)*(k-s))%N
    print("通过泄露k,计算出的私钥为：",private_key)
    
def sm2_sign_reusing_k(private_key, message, k):
    S = ECC_mul(k, G)
    Z = hashlib.sha256(message).digest()
    e = int.from_bytes(Z, 'big') % N
    k_inv = Multi_inverse(k, N)
    r = (e + S[0]) % N
    s_inv = Multi_inverse(1+private_key, N)
    s = (s_inv * (k - r * private_key)) % N
    return r, s

def reusing_k(r1,s1,r2,s2):
    temp=(s1-s2+r1-r2)
    private_key=((s2-s1)*Multi_inverse(temp, N))%N
    print("通过重用k,计算出的私钥为：",private_key)

def two_user_same_k(r1,s1,r2,s2,k):
    private_key1=((k-s1)*Multi_inverse(s1+r1, N))%N
    print("user2可以推出，user1的私钥为：",private_key1)
    private_key2=((k-s2)*Multi_inverse(s2+r2, N))%N
    print("user1可以推出，user2的私钥为：",private_key2)
    
    
    
prikey = 0x5f6717883bef25f45a129c11fcac1567d74bda5a9ad4cbffc8203c0da2a1473c
pubkey = ECC_mul(prikey, G)
#print("私钥为：",prikey)
message1 = b"SM2 scheme"
message2=b"happy hippo"

#泄露k
#r,s,k=sm2_sign_leaking_k(prikey, message)
#leaking_k_gen_prikey(r,s,k)

#重用k
#k = rfc6979_generate_k(hashlib.sha256, prikey, message1, N)
#r1,s1=sm2_sign_reusing_k(prikey, message1,k)
#r2,s2=sm2_sign_reusing_k(prikey, message2,k)
#reusing_k(r1,s1,r2,s2)

#2名用户用同样的k
prikey2 = 0xbf2e30f07dde4a8a9425302399582acd49b75ab353a99ff90407b81b4514287a
print("user1的私钥为：",prikey)
print("user2的私钥为：",prikey2)
k = rfc6979_generate_k(hashlib.sha256, prikey, message1, N)
r1,s1=sm2_sign_reusing_k(prikey, message1,k)
r2,s2=sm2_sign_reusing_k(prikey2, message2,k)
two_user_same_k(r1,s1,r2,s2,k)



#print("对消息签名中……")
#print("签名为:(",r,",",s,")")
#print("对签名验证中……")
#sm2_Verify(r,s, message,pubkey)
