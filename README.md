# No.61-孔婧

## 🎖️project01 implement the naïve birthday attack of reduced SM3 ✔️
说明：<br>
生日攻击是一种利用生日悖论的攻击方式，针对哈希算法。生日悖论指的是，随着数据量的增加，出现两个不同输入具有相同哈希值的概率逐渐增加。在SM3生日攻击中，我会生成一系列随机字符串，并计算其SM3哈希值的前n位。通过大量的随机字符串生成和比较，试图找到两个不同的字符串，其前n位哈希值相同，从而达到生日攻击的目的。<br>
生日攻击过程如下：<br>
>1.	构造消息：<br>
从可能的输入空间中生成两个随机消息，这两个消息需要满足相同的hash要求。<br>
>2.	计算hash：<br>
>每次对这两个不同的消息进行SM3算法的运算，生成相应的hash值。<br>
>3.	查找碰撞：<br>
>通过比较看这两个不同的随机消息的hash值的前n位是否相同，如果相同，则攻击成功；如果不同，则攻击失败，需重新生成两个随机消息，并再进行2、3步。<br>
>注：改变n即可实现前任意位的生日攻击。birthdayAttack(n)这里输入的数实现的是前几个字节的碰撞，实际上是实现了前四倍输入的数位bit的碰撞，例如令n=8实际上是实现了前32位bit的碰撞。<br>

实现方式：本项目用c++完成。<br>
运行结果：<br>
在此以实现了前20位bit的碰撞为例展示结果：<br>



## 🎖️project02 implement the Rho method of reduced SM3✔️

## 🎖️Project3: implement length extension attack for SM3, SHA256, etc.✔️

## 🎖️Project4: do your best to optimize SM3 implementation (software)✔️

## 🎖️project08 AES impl with ARM instruction ✔️

实现方式：<br>
我使用ARMv8—AES内部函数，以实现在ARMv8架构上进行AES加密和解密操作<br>
通过在[指令集网站](https://developer.arm.com/architectures/instruction-sets/intrinsics/#q=AES)中查阅，主要使用的函数定义如下：<br>

>// 执行AES单轮加密( AddRoundKey, SubBytes 和 ShiftRows )<br>
>uint8x16_t vaeseq_u8(uint8x16_t data, uint8x16_t key);<br>
>// 执行AES混淆列（mix columns）<br>
>uint8x16_t vaesmcq_u8(uint8x16_t data);<br>

## 🎖️project09 AES / SM4 software implementation✔️

### AES实现✔️

![IMG_2377(20230727-004119)](C:\Users\86130\Desktop\IMG_2377(20230727-004119).PNG)



运行结果：[运行测试]([E:\创新创业实践\代码仓\Project_09\AES\运行测试.png](https://github.com/happyhippo111/No.61-/blob/main/Project_09/AES/%E8%BF%90%E8%A1%8C%E6%B5%8B%E8%AF%95.png))

### SM4实现✔️

算法流程图：![算法流程图](E:\创新创业实践\代码仓\Project_09\SM4\算法流程图.png)

解密变换与加密变换结构相同，不同的仅是轮密钥的使用顺序。(解密时，使用轮密钥序 rk31,rk30,⋯,rk0)<br>
运行结果：![运行结果](E:\创新创业实践\代码仓\Project_09\SM4\运行结果.jpg)









# 待完成

修补project9

开始比特币
