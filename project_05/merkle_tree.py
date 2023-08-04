from hashlib import sha256
import random

def SHA256(s):
    return sha256(s.encode('utf-8')).hexdigest()

class Merkletree:
    def __init__(self):
        self.leaves = []
        self.levels = None
        self.root = None

    def add(self):
        num = len(self.levels[0])
        flag = None
        if num % 2 == 1:  
            num -= 1
            flag = self.levels[0][-1]
        lst = []
        for z, y in zip(self.levels[0][0:num:2], self.levels[0][1:num:2]):
            lst.append(SHA256('0x01'+ z + y))
        if flag is not None:
            lst.append(flag)
        self.levels = [lst, ] + self.levels

    def creat(self,L):
        for i in L:
            i = SHA256('0x00' + i)
            self.leaves.append(i)
        if len(self.leaves) > 0:
            self.levels = [self.leaves, ]
            while len(self.levels[0]) > 1:
                self.add()
        print("创建成功")
        print("这个merkle树的根为：")
        self.root=self.levels[0][0]
        print(self.root)
        
    def p(self, x):
        path = []
        for i in range(len(self.levels) - 1, 0, -1):
            t = len(self.levels[i]) 
            if (x == t - 1) and (t % 2 == 1):  
                x = int(x / 2.)  
                continue
            if x % 2 :  
                s = x - 1
                q = "左"
            else:
                s = x + 1
                q = "右"
            path.append((q, self.levels[i][s]))
            x = int(x / 2.)
        return path

    def proof(self, p, h, root):
        hash=h
        for i in p:
            f = i[0]
            v = i[1]
            if f == '左':
                hash = SHA256('0x01'+ v + hash)
            else:
                hash = SHA256('0x01'+ hash + v)
        if hash == root:
            return True
        else:
            return False


L = []
for i in range(100000):
    L.append(str(i))
t = Merkletree()
t.creat(L)
print("证明50在树中：")
p1 = t.p(50) #可改
h1 = t.levels[-1][50]
if t.proof(p1, h1, t.root):
    print("证明成功")
    print('路径为：','\n', p1)
print("证明66.5不在树中：")
p2 = t.p(66) 
h2 = t.levels[-1][66]
p3 = t.p(67) 
h3 = t.levels[-1][67]
if t.proof(p2, h2, t.root) and t.proof(p3, h3, t.root):
    print("证明成功")
    
