import hashlib
import random
import secp256k1
import time

prikey = secp256k1.Fr(0x5f6717883bef25f45a129c11fcac1567d74bda5a9ad4cbffc8203c0da2a1473c)
pubkey = secp256k1.G * prikey

def Hash_of_messages(file):
    with open(file, 'rb') as f:#'./测试文件1.txt'
        m = int.from_bytes(hashlib.sha256(f.read()).digest(), 'little')
        m = secp256k1.Fr(m)
    #print(f'hash={m}')
    return m
        
def schnorr_sign(file):
# R = k ∗ G
# e = hash(R || m)
# s = k + e ∗ prikey
    m=Hash_of_messages(file)
    k = secp256k1.Fr(random.randint(0, secp256k1.N))
    R = secp256k1.G * k
    hasher = hashlib.sha256()
    hasher.update(R.x.x.to_bytes(32, 'little'))
    hasher.update(R.y.x.to_bytes(32, 'little'))
    hasher.update(m.x.to_bytes(32, 'little'))
    e = secp256k1.Fr(int.from_bytes(hasher.digest(), 'little'))
    s = k + e * prikey
    #print(f'sign=(R={R}, s={s})')
    return R,s

def verify_single(file,R,s,):
    m=Hash_of_messages(file)
    hasher = hashlib.sha256()
    hasher.update(R.x.x.to_bytes(32, 'little'))
    hasher.update(R.y.x.to_bytes(32, 'little'))
    hasher.update(m.x.to_bytes(32, 'little'))
    e = secp256k1.Fr(int.from_bytes(hasher.digest(), 'little'))
    verify = secp256k1.G * s == R + pubkey * e
    print(f'verify={verify}',)
    # s ∗ G =? R + hash(R || m) ∗ P

def verify_Batch(num,filelist,Rlist,slist):
    elist=[0]*num
    for i in range(num):
        m=Hash_of_messages(filelist[i])
        hasher = hashlib.sha256()
        hasher.update(Rlist[i].x.x.to_bytes(32, 'little'))
        hasher.update(Rlist[i].y.x.to_bytes(32, 'little'))
        hasher.update(m.x.to_bytes(32, 'little'))
        elist[i]= secp256k1.Fr(int.from_bytes(hasher.digest(), 'little'))  
    a=[0]*(num)
    sum_aisi=slist[0]
    sum_aiRi=Rlist[0]
    print(Rlist[0])
    sum_aiei=elist[0]
    for i in range(1,num):
        a[i]=secp256k1.Fr(random.randint(0, secp256k1.N))
        sum_aisi+=a[i]*slist[i]
        sum_aiRi+=Rlist[i]*a[i]
        sum_aiei+=a[i]*elist[i]
    verify = secp256k1.G *sum_aisi == sum_aiRi + pubkey * sum_aiei
    print(f'verify={verify}',"\n")
    
time_start = time.time() #开始计时
for i in range(9):
    R,s=schnorr_sign('./测试文件1.txt')
    verify_single('./测试文件1.txt',R,s,)
time_end = time.time()#结束计时
time_c= time_end - time_start
print('time cost', time_c, 's')

filelist=['./测试文件1.txt','./测试文件2.txt','./测试文件3.txt','./测试文件1.txt','./测试文件2.txt','./测试文件3.txt','./测试文件1.txt','./测试文件2.txt','./测试文件3.txt']
num=9
Rlist=[0]*num
slist=[0]*num
for i in range(num):
        Rlist[i],slist[i]=schnorr_sign(filelist[i])
print(slist)
time_start = time.time() #开始计时
verify_Batch(num,filelist,Rlist,slist)
time_end = time.time()#结束计时
time_c= time_end - time_start
print('time cost', time_c, 's')



