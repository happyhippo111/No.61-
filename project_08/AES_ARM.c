#include <stdint.h>
#include <arm_neon.h>
#include <arm_acle.h>

void aes_process_arm(const uint8_t key[], const uint8_t subkeys[], uint32_t rounds,
	const uint8_t input[], uint8_t output[], uint32_t length)
{
	while (length >= 16)
	{
		uint8x16_t block = vld1q_u8(input);

		// AES 单轮加密
		block = vaeseq_u8(block, vld1q_u8(key));
		// AES列混合
		block = vaesmcq_u8(block);

		
		block = vaeseq_u8(block, vld1q_u8(subkeys));
		block = vaesmcq_u8(block);

		for (unsigned int i = 1; i < rounds - 2; ++i)
		{
			
			block = vaeseq_u8(block, vld1q_u8(subkeys + i * 16));
			block = vaesmcq_u8(block);
		}

		block = vaeseq_u8(block, vld1q_u8(subkeys + (rounds - 2) * 16));
		// 比特异或
		block = veorq_u8(block, vld1q_u8(subkeys + (rounds - 1) * 16));

		vst1q_u8(output, block);

		input += 16; output += 16;
		length -= 16;
	}
}

int main(int argc, char* argv[])
{
	const uint8_t input[16] = { 
		0x32, 0x43, 0xf6, 0xa8, 0x88, 0x5a, 0x30, 0x8d, 0x31, 0x31, 0x98, 0xa2, 0xe0, 0x37, 0x07, 0x34
	};

	const uint8_t key[16] = { 
		0x2b, 0x7e, 0x15, 0x16, 0x28, 0xae, 0xd2, 0xa6, 0xab, 0xf7, 0x15, 0x88, 0x9 , 0xcf, 0x4f, 0x3c
	};

		const uint8_t subkeys[10][16] = {
			{0xA0, 0xFA, 0xFE, 0x17, 0x88, 0x54, 0x2c, 0xb1, 0x23, 0xa3, 0x39, 0x39, 0x2a, 0x6c, 0x76, 0x05},
			{0xF2, 0xC2, 0x95, 0xF2, 0x7a, 0x96, 0xb9, 0x43, 0x59, 0x35, 0x80, 0x7a, 0x73, 0x59, 0xf6, 0x7f},
			{0x3D, 0x80, 0x47, 0x7D, 0x47, 0x16, 0xFE, 0x3E, 0x1E, 0x23, 0x7E, 0x44, 0x6D, 0x7A, 0x88, 0x3B},
			{0xEF, 0x44, 0xA5, 0x41, 0xA8, 0x52, 0x5B, 0x7F, 0xB6, 0x71, 0x25, 0x3B, 0xDB, 0x0B, 0xAD, 0x00},
			{0xD4, 0xD1, 0xC6, 0xF8, 0x7C, 0x83, 0x9D, 0x87, 0xCA, 0xF2, 0xB8, 0xBC, 0x11, 0xF9, 0x15, 0xBC},
			{0x6D, 0x88, 0xA3, 0x7A, 0x11, 0x0B, 0x3E, 0xFD, 0xDB, 0xF9, 0x86, 0x41, 0xCA, 0x00, 0x93, 0xFD},
			{0x4E, 0x54, 0xF7, 0x0E, 0x5F, 0x5F, 0xC9, 0xF3, 0x84, 0xA6, 0x4F, 0xB2, 0x4E, 0xA6, 0xDC, 0x4F},
			{0xEA, 0xD2, 0x73, 0x21, 0xB5, 0x8D, 0xBA, 0xD2, 0x31, 0x2B, 0xF5, 0x60, 0x7F, 0x8D, 0x29, 0x2F},
			{0xAC, 0x77, 0x66, 0xF3, 0x19, 0xFA, 0xDC, 0x21, 0x28, 0xD1, 0x29, 0x41, 0x57, 0x5c, 0x00, 0x6E},
			{0xD0, 0x14, 0xF9, 0xA8, 0xC9, 0xEE, 0x25, 0x89, 0xE1, 0x3F, 0x0c, 0xC8, 0xB6, 0x63, 0x0C, 0xA6}
	};

	 
	uint8_t output[19] = { 0 };

	aes_arm((const uint8_t*)key, (const uint8_t*)subkeys, 10, input, output + 3, 16);
	printf("输出: ");
	for (unsigned int i = 3; i < 19; ++i)
		printf("%02X ", output[i],'/n');

	return 0;
}
