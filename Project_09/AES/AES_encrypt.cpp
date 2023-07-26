#include <iostream>
#include "aes.h"

using namespace std;


void AddRoundKey(unsigned char* state, unsigned char* roundKey) {
	for (int i = 0; i < 16; i++) {
		state[i] ^= roundKey[i];
	}
}

void SubBytes(unsigned char* state) {
	for (int i = 0; i < 16; i++) {
		state[i] = s[state[i]];
	}
}

void ShiftRows(unsigned char* state) {
	unsigned char tmp[16];

	/* Column 1 */
	tmp[0] = state[0];
	tmp[1] = state[5];
	tmp[2] = state[10];
	tmp[3] = state[15];

	/* Column 2 */
	tmp[4] = state[4];
	tmp[5] = state[9];
	tmp[6] = state[14];
	tmp[7] = state[3];

	/* Column 3 */
	tmp[8] = state[8];
	tmp[9] = state[13];
	tmp[10] = state[2];
	tmp[11] = state[7];

	/* Column 4 */
	tmp[12] = state[12];
	tmp[13] = state[1];
	tmp[14] = state[6];
	tmp[15] = state[11];

	for (int i = 0; i < 16; i++) {
		state[i] = tmp[i];
	}
}
/*列混合——使用查找表来加速*/
void MixColumns(unsigned char* state) {
	unsigned char tmp[16];

	tmp[0] = (unsigned char)mul2[state[0]] ^ mul3[state[1]] ^ state[2] ^ state[3];
	tmp[1] = (unsigned char)state[0] ^ mul2[state[1]] ^ mul3[state[2]] ^ state[3];
	tmp[2] = (unsigned char)state[0] ^ state[1] ^ mul2[state[2]] ^ mul3[state[3]];
	tmp[3] = (unsigned char)mul3[state[0]] ^ state[1] ^ state[2] ^ mul2[state[3]];

	tmp[4] = (unsigned char)mul2[state[4]] ^ mul3[state[5]] ^ state[6] ^ state[7];
	tmp[5] = (unsigned char)state[4] ^ mul2[state[5]] ^ mul3[state[6]] ^ state[7];
	tmp[6] = (unsigned char)state[4] ^ state[5] ^ mul2[state[6]] ^ mul3[state[7]];
	tmp[7] = (unsigned char)mul3[state[4]] ^ state[5] ^ state[6] ^ mul2[state[7]];

	tmp[8] = (unsigned char)mul2[state[8]] ^ mul3[state[9]] ^ state[10] ^ state[11];
	tmp[9] = (unsigned char)state[8] ^ mul2[state[9]] ^ mul3[state[10]] ^ state[11];
	tmp[10] = (unsigned char)state[8] ^ state[9] ^ mul2[state[10]] ^ mul3[state[11]];
	tmp[11] = (unsigned char)mul3[state[8]] ^ state[9] ^ state[10] ^ mul2[state[11]];

	tmp[12] = (unsigned char)mul2[state[12]] ^ mul3[state[13]] ^ state[14] ^ state[15];
	tmp[13] = (unsigned char)state[12] ^ mul2[state[13]] ^ mul3[state[14]] ^ state[15];
	tmp[14] = (unsigned char)state[12] ^ state[13] ^ mul2[state[14]] ^ mul3[state[15]];
	tmp[15] = (unsigned char)mul3[state[12]] ^ state[13] ^ state[14] ^ mul2[state[15]];

	for (int i = 0; i < 16; i++) {
		state[i] = tmp[i];
	}
}


void Round(unsigned char* state, unsigned char* key) {
	SubBytes(state);
	ShiftRows(state);
	MixColumns(state);
	AddRoundKey(state, key);
}

// 最后一轮加密没有列混合
void FinalRound(unsigned char* state, unsigned char* key) {
	SubBytes(state);
	ShiftRows(state);
	AddRoundKey(state, key);
}


void AESEncrypt(unsigned char* message, unsigned char* expandedKey, unsigned char* encryptedMessage) {
	unsigned char state[16]; // 存储原始信息的前 16 个字节

	for (int i = 0; i < 16; i++) {
		state[i] = message[i];
	}

	int numberOfRounds = 9;

	AddRoundKey(state, expandedKey); // Initial round

	for (int i = 0; i < numberOfRounds; i++) {
		Round(state, expandedKey + (16 * (i + 1)));
	}

	FinalRound(state, expandedKey + 160);

	//将加密状态复制到缓冲区
	for (int i = 0; i < 16; i++) {
		encryptedMessage[i] = state[i];
	}
}

int main() {

	cout << "   128-bit AES 加密  " << endl;

	char message[1024] = "kongjing202122202212";

	/*
	cout << "请输入要加密的信息: ";
	cin.getline(message, sizeof(message));
	cout << message << endl;
	*/
	// 填充
	clock_t start_time = clock();
	for (int i = 0;i < 100;i++) {

		int originalLen = strlen((const char*)message);

		int paddedMessageLen = originalLen;

		if ((paddedMessageLen % 16) != 0) {
			paddedMessageLen = (paddedMessageLen / 16 + 1) * 16;
		}

		unsigned char* paddedMessage = new unsigned char[paddedMessageLen];
		for (int i = 0; i < paddedMessageLen; i++) {
			if (i >= originalLen) {
				paddedMessage[i] = 0;
			}
			else {
				paddedMessage[i] = message[i];
			}
		}


		unsigned char* encryptedMessage = new unsigned char[paddedMessageLen];
		unsigned char key[16] = { 0x66,0x08,0x89,0xab,0x8c,0x6b,0x67,0xb8,0xf0,0xf6,0xe9,0x15,0x6a,0xb5,0xe5,0xc8 };
		unsigned char expandedKey[176];

		KeyExpansion(key, expandedKey);

		for (int i = 0; i < paddedMessageLen; i += 16) {
			AESEncrypt(paddedMessage + i, expandedKey, encryptedMessage + i);
		}


		delete[] paddedMessage;
		delete[] encryptedMessage;
	}
	clock_t end_time = clock();
	double duration = double(end_time - start_time) / CLOCKS_PER_SEC;
	/*
	cout << "加密后的数据:" << endl;
	for (int i = 0; i < paddedMessageLen; i++) {
		cout << hex << (int)encryptedMessage[i];
		cout << " " ;
	}
	*/
	cout << "加密所用时间：" << duration << end_time << endl;



	return 0;

}