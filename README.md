# No.61-孔婧

## 🎖️project01 implement the naïve birthday attack of reduced SM3 ✔️

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



运行结果：![运行测试](E:\创新创业实践\代码仓\Project_09\AES\运行测试.png)

### SM4实现✔️

算法流程图：![算法流程图](E:\创新创业实践\代码仓\Project_09\SM4\算法流程图.png)

解密变换与加密变换结构相同，不同的仅是轮密钥的使用顺序。(解密时，使用轮密钥序 rk31,rk30,⋯,rk0)<br>
运行结果：![运行结果](E:\创新创业实践\代码仓\Project_09\SM4\运行结果.jpg)









# 待完成

修补project9

开始比特币
