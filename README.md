# No.61-孔婧

## 🎖️project_01 implement the naïve birthday attack of reduced SM3 ✔️
生日攻击是一种利用生日悖论的攻击方式，针对哈希算法。生日悖论指的是，随着数据量的增加，出现两个不同输入具有相同哈希值的概率逐渐增加。在SM3生日攻击中，我会生成一系列随机字符串，并计算其SM3哈希值的前n位。通过大量的随机字符串生成和比较，试图找到两个不同的字符串，其前n位哈希值相同，从而达到生日攻击的目的。<br>
生日攻击过程如下：<br>
>1.	构造消息：<br>
从可能的输入空间中生成两个随机消息，这两个消息需要满足相同的hash要求。<br>
>2.	计算hash：<br>
每次对这两个不同的消息进行SM3算法的运算，生成相应的hash值。<br>
>3.	查找碰撞：<br>
通过比较看这两个不同的随机消息的hash值的前n位是否相同，如果相同，则攻击成功；如果不同，则攻击失败，需重新生成两个随机消息，并再进行2、3步。<br>

注：改变n即可实现前任意位的生日攻击。birthdayAttack(n)这里输入的数实现的是前几个字节的碰撞，实际上是实现了前四倍输入的数位bit的碰撞，例如令n=8实际上是实现了前32位bit的碰撞。<br>

实现方式：本项目用c++完成。<br>
运行结果：在此以实现了前20位bit的碰撞为例展示结果：<br>
![Alt text](https://github.com/happyhippo111/No.61-/blob/main/project_01/%E8%BF%90%E8%A1%8C%E7%BB%93%E6%9E%9C.png)



## 🎖️project_02 implement the Rho method of reduced SM3✔️
原理：<br>
>Rho攻击是一种快速碰撞攻击。在SM3 Rho攻击中，生成大量随机字符串，并计算它们的SM3哈希值的前n位比特。将这些前n位哈希值存储在vector a中。然后，当遇到新的哈希值时，检查它是否在vector a中。如果找到两个不同的字符串，其前n位哈希值相同，则我们认为攻击成功。<br>

步骤：
>首先创建一个空的字符串向量a，用于存储每次生成随机字符串经过哈希后的结果的前n/4位。使用循环生成大量随机字符串，并对每个随机字符串进行哈希，提取出前n/4位。
>判断提取出的前n/4位是否在字符串向量a中出现过，若出现过，则说明发生了哈希冲突，攻击成功，输出冲突字符串和哈希值。
>如果没有冲突，则将提取出的哈希结果前n/4位加入字符串向量a中，并继续下一轮生成随机字符串的尝试。如果攻击失败，继续循环直至成功。<br>

注意：存储每次生成随机字符串经过哈希后的结果的前n/4位的原因：rho_attack(n)的n的单位是bit，生成随机字符串的单位是字节。<br>
实现方式：本项目用c++完成。<br>
运行结果：在此以实现了前40位bit的rho攻击为例展示结果<br>
![Alt text](https://github.com/happyhippo111/No.61-/blob/main/project_02/%E8%BF%90%E8%A1%8C%E7%BB%93%E6%9E%9C.png)
![Alt text](https://github.com/happyhippo111/No.61-/blob/main/project_02/%E8%BF%90%E8%A1%8C%E7%BB%93%E6%9E%9C(1).png)

## 🎖️Project_03: implement length extension attack for SM3, SHA256, etc.✔️
SM3为MD结构，计算原理大致如下：
![Alt text](https://github.com/happyhippo111/No.61-/blob/main/project_03/%E8%AE%A1%E7%AE%97%E5%8E%9F%E7%90%86.png)
本项目利用了SM3的MD结构的特点，实现了SM3的长度扩展攻击，主要需完成下面几步：
>1.	随机生成一个消息作为原始消息m，用SM3函数算出其hash值(h)，并算出其length值。
>2.	随意选取一个附加消息。首先用h推算出这一次加密结束后8个向量的值，再以它们作为初始向量，去加密附加消息，得到其hash值(暂用hash1指代)。
>3.	计算m+ padding + 附加消息的hash值(暂用hash2指代)，比较hash1与hash2，如果hash1和hash2相等，则对SM3的长度攻击成功。

实现方式：本项目用c++完成。<br>
运行结果：<br>
![Alt text](https://github.com/happyhippo111/No.61-/blob/main/project_03/%E8%BF%90%E8%A1%8C%E7%BB%93%E6%9E%9C.png)
## 🎖️Project_04: do your best to optimize SM3 implementation (software)✔️

## 🎖️project_08 AES impl with ARM instruction ✔️

实现方式：<br>
我使用ARMv8—AES内部函数，以实现在ARMv8架构上进行AES加密和解密操作<br>
通过在[指令集网站](https://developer.arm.com/architectures/instruction-sets/intrinsics/#q=AES)中查阅，主要使用的函数定义如下：<br>

>// 执行AES单轮加密( AddRoundKey, SubBytes 和 ShiftRows )<br>
>uint8x16_t vaeseq_u8(uint8x16_t data, uint8x16_t key);<br>
>// 执行AES混淆列（mix columns）<br>
>uint8x16_t vaesmcq_u8(uint8x16_t data);<br>

该项目使用C语言编程完成

## 🎖️project_09 AES / SM4 software implementation✔️

### AES实现✔️

![Alt text](https://github.com/happyhippo111/No.61-/blob/main/project_09/AES/IMG_2377(20230727-004119).PNG)
实现方式:<br>
根据上述流程图使用C++完成<br>

运行结果：![Alt text](https://github.com/happyhippo111/No.61-/blob/main/project_09/AES/%E8%BF%90%E8%A1%8C%E6%B5%8B%E8%AF%95.png)
### SM4实现✔️

算法流程图：![Alt text](https://github.com/happyhippo111/No.61-/blob/main/project_09/SM4/%E7%AE%97%E6%B3%95%E6%B5%81%E7%A8%8B%E5%9B%BE.png)

解密变换与加密变换结构相同，不同的仅是轮密钥的使用顺序。(解密时，使用轮密钥序 rk31,rk30,⋯,rk0)<br>
实现方式：使用C++实现<br>
运行结果：![Alt text](https://github.com/happyhippo111/No.61-/blob/main/project_09/SM4/%E8%BF%90%E8%A1%8C%E7%BB%93%E6%9E%9C.jpg)
## 🎖️project_18 send a tx on Bitcoin testnet, and parse the tx data down to every bit, better write script yourself✔️
实现方式：<br>
生成比特币测试地址，记录图中出现的地址和私钥：<br>
![Alt text](https://github.com/happyhippo111/No.61-/blob/main/project_18/%E6%B5%8B%E8%AF%95%E7%89%88%E5%9C%B0%E5%9D%80.png)
登录比特币的测试币水龙头，获取一定数量的测试用币<br>

![Alt text](https://github.com/happyhippo111/No.61-/blob/main/project_18/%E8%8E%B7%E5%8F%96%E6%B5%8B%E8%AF%95%E5%B8%81.png)

进入[网站](https://live.blockcypher.com/)，查询我的账户交易信息和刚刚的交易记录

![Alt text](https://github.com/happyhippo111/No.61-/blob/main/project_18/%E8%B4%A6%E6%88%B7%E8%AE%B0%E5%BD%95.png)

![Alt text](https://github.com/happyhippo111/No.61-/blob/main/project_18/%E4%BA%A4%E6%98%93%E4%BF%A1%E6%81%AF.png)

使用python自写脚本，可以解析获取该交易的详细信息<br>
脚本运行结果如下：<br>

![Alt text](https://github.com/happyhippo111/No.61-/blob/main/project_18/%E8%84%9A%E6%9C%AC%E8%BF%90%E8%A1%8C%E7%BB%93%E6%9E%9C.png)

完整爬取内容请见文件夹内parsed tx data.md文件<br>
在tx里面可以看到交易的地址、id、哈希值，交易时间、交易金额、是否双花等信息<br>

## 🎖️project_19 forge a signature to pretend that you are Satoshi✔️
实现方式：<br>
R = H(m)/s * G + r/s * P<br>
如果令 u = H(m)/s, v = r/s，<br>
那么 R = uG + vP<br>
通过随机生成u、v的值u'，v'，使得：<br>
u'G + v'P = R'<br>
计算出 r' = R'.x， 从而得到 s' = r'/v， H(m') = u * s'<br>
那么对于消息m'，其签名结果为：(r', s')。此签名是可以通过验证检查，所以有效。<br>

这个操作其实有点类似于签名延展性，没有通过私钥，利用已有合法签名构造另外的有效签名。<br>
这个项目使用之前写过的ECDSA.py作为签名库，通过python编程实现伪造<br>
运行结果：![Alt text](https://github.com/happyhippo111/No.61-/blob/main/project_19/%E8%BF%90%E8%A1%8C%E7%BB%93%E6%9E%9C.jpg)






# 待完成

修补project9

开始比特币
