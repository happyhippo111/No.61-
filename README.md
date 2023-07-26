# No.61-孔婧

## project08 AES impl with ARM instruction
我使用ARMv8—AES内部函数，以实现在ARMv8架构上进行AES加密和解密操作<br>
通过在[指令集网站](https://developer.arm.com/architectures/instruction-sets/intrinsics/#q=AES)中查阅，主要使用的函数定义如下：<br>
// 执行AES单轮加密( AddRoundKey, SubBytes 和 ShiftRows )<br>
uint8x16_t vaeseq_u8(uint8x16_t data, uint8x16_t key);<br>
// 执行AES混淆列（mix columns）<br>
uint8x16_t vaesmcq_u8(uint8x16_t data);<br>
