# No.61-孔婧

## project08 AES impl with ARM instruction
实现方式：<br>
我使用ARMv8—AES内部函数，以实现在ARMv8架构上进行AES加密和解密操作<br>
通过在[指令集网站](https://developer.arm.com/architectures/instruction-sets/intrinsics/#q=AES)中查阅，主要使用的函数定义如下：<br>
>// 执行AES单轮加密( AddRoundKey, SubBytes 和 ShiftRows )<br>
uint8x16_t vaeseq_u8(uint8x16_t data, uint8x16_t key);<br>
// 执行AES混淆列（mix columns）<br>
uint8x16_t vaesmcq_u8(uint8x16_t data);<br>

## project09 AES / SM4 software implementation
算法流程图
分组大小：SM4算法以128位（16字节）为一个分组进行加密和解密操作。<br>
密钥长度：SM4支持128位（16字节）密钥长度，也就是说密钥由128位的比特组成。<br>
轮数：SM4使用32轮迭代，每轮都进行不同的代换和置换操作。<br>
S-Box：SM4使用了一个固定的非线性变换（S-Box）表，对输入进行替换操作，增加算法的混淆性和扩散性。<br>
T-Box（线性移位）：SM4还使用一个T-Box函数，对输入进行线性变换，进一步增强了算法的扩散性。<br>
Feistel结构：SM4采用了Feistel结构，将输入分为左右两部分，通过不同的轮函数进行迭代混淆和扩散。<br>
加解密一致性：解密变换与加密变换结构相同，不同的仅是轮密钥的使用顺序。(解密时，使用轮密钥序 rk31,rk30,⋯,rk0)<br>
运行结果：


