// project3SM3.cpp : 此文件包含 "main" 函数。程序执行将在此处开始并结束。
//

#include <iostream>
#include <vector>
#include <string>
#include <sstream>
#include <random>
#include <iomanip>

using namespace std;
int T[64];
int W1[68];
int W2[64];

void init_T()
{
	for (int i = 0; i <= 15; i++)
		T[i] = 0x79CC4519;
	for (int i = 16; i <= 63; i++)
		T[i] = 0x7A879D8A;
}


unsigned int FF(unsigned int x, unsigned int y, unsigned int z, int j)
{
	if (0 <= j && j <= 15)
		return x ^ y ^ z;
	else if (16 <= j && j <= 63)
		return (x & y) | (x & z) | (y & z);
	return 0;
}

unsigned int GG(unsigned int x, unsigned int y, unsigned int z, int j)
{
	if (0 <= j && j <= 15)
		return x ^ y ^ z;
	else if (16 <= j && j <= 63)
		return (x & y) | ((~x) & z);
	return 0;
}

unsigned int left_(unsigned int x, unsigned int n)
{
	n = n % 32;
	return ((x << n) & 0xFFFFFFFF | ((x & 0xFFFFFFFF) >> (32 - n)));
}

unsigned int P0(unsigned int x)
{
	return x ^ (left_(x, 9)) ^ (left_(x, 17));
}

unsigned int P1(unsigned int x)
{
	return x ^ (left_(x, 15)) ^ (left_(x, 23));
}

vector<string> cut(const string& text, int num) {
	vector<string> m;
	for (int i = 0; i < text.length(); i += num) {
		m.push_back(text.substr(i, num));
	}
	return m;
}

string DecToHex(int str) {
	string hex = "";
	int temp = 0;
	while (str >= 1) {
		temp = str % 16;
		if (temp < 10 && temp >= 0) {
			hex = to_string(temp) + hex;
		}
		else {
			hex += ('a' + (temp - 10));
		}
		str = str / 16;
	}
	return hex;
}

string pad(string str) {
	string res = "";
	for (int i = 0; i < str.size(); i++) {
		if (str[i] == '\0')
			res += "00";
		if (str[i] == 'Ç')
			res += "80";
		else
		    res += DecToHex((int)str[i]);
	}
	int res_length = res.size() * 4;
	res += "8";
	while (res.size() % 128 != 112) {
		res += "0";
	}
	string res_len = DecToHex(res_length);
	while (res_len.size() != 16) {
		res_len = "0" + res_len;
	}
	res += res_len;
	return res;
}

string BinToHex(string str) {
	string hex = "";
	int temp = 0;
	while (str.size() % 4 != 0) {
		str = "0" + str;
	}
	for (int i = 0; i < str.size(); i += 4) {
		temp = (str[i] - '0') * 8 + (str[i + 1] - '0') * 4 + (str[i + 2] - '0') * 2 + (str[i + 3] - '0') * 1;
		if (temp < 10) {
			hex += to_string(temp);
		}
		else {
			hex += 'a' + (temp - 10);
		}
	}
	return hex;
}


string HexToBin(string str) {
	string bin = "";
	string table[16] = { "0000","0001","0010","0011","0100","0101","0110","0111","1000","1001","1010","1011","1100","1101","1110","1111" };
	for (int i = 0; i < str.size(); i++) {
		if (str[i] >= 'a' && str[i] <= 'f') {
			bin += table[str[i] - 'a' + 10];
		}
		else {
			bin += table[str[i] - '0'];
		}
	}
	return bin;
}


string L(string str, int len) {
	string res = HexToBin(str);
	res = res.substr(len) + res.substr(0, len);
	return BinToHex(res);
}

string XOR(string str1, string str2) {
	string res1 = HexToBin(str1);
	string res2 = HexToBin(str2);
	string res = "";
	for (int i = 0; i < res1.size(); i++) {
		if (res1[i] == res2[i]) {
			res += "0";
		}
		else {
			res += "1";
		}
	}
	return BinToHex(res);
}

string P1_(string str) {
	return XOR(XOR(str, L(str, 15)), L(str, 23));
}

int hexToDecimal(const string& hexString) {
	int decimalValue = 0;
	int power = 1;
	for (int i = hexString.size() - 1; i >= 0; --i) {
		char c = hexString[i];
		int digit;
		if (c >= '0' && c <= '9') {
			digit = c - '0';
		}
		else if (c >= 'A' && c <= 'F') {
			digit = c - 'A' + 10;
		}
		else if (c >= 'a' && c <= 'f') {
			digit = c - 'a' + 10;
		}
		else {
			cout << "Invalid hex string" << endl;
			return 0;
		}
		decimalValue += digit * power;
		power *= 16;
	}
	return decimalValue;
}


string CF(const string& iv, const string& m)
{
	string res = m;
	for (int i = 16; i < 68; i++) {
		res += XOR(XOR(P1_(XOR(XOR(res.substr((i - 16) * 8, 8), res.substr((i - 9) * 8, 8)), L(res.substr((i - 3) * 8, 8), 15))), L(res.substr((i - 13) * 8, 8), 7)), res.substr((i - 6) * 8, 8));
	}
	for (int i = 0; i < 64; i++) {
		res += XOR(res.substr(i * 8, 8), res.substr((i + 4) * 8, 8));
	}
	vector<string> W = cut(res, 8);
	for (int i = 0; i < 68; i++) {
		W1[i] = hexToDecimal(W[i]);
	}
	for (int i = 68; i < 132; i++) {
		W2[i - 68] = hexToDecimal(W[i]);
	}
	unsigned int A[8];
	unsigned int SS1, SS2, TT1, TT2;
	vector<string> B = cut(iv, 8);
	for (int i = 0; i < 8; i++) {
		A[i] = hexToDecimal(B[i]);
	}
	for (int j = 0; j < 64; j++)
	{
		SS1 = left_((left_(A[0], 12)) + A[4] + (left_(T[j], j)), 7);
		SS2 = SS1 ^ (left_(A[0], 12));
		TT1 = FF(A[0], A[1], A[2], j) + A[3] + SS2 + W2[j];
		TT2 = GG(A[4], A[5], A[6], j) + A[7] + SS1 + W1[j];
		A[3] = A[2];
		A[2] = left_(A[1], 9);
		A[1] = A[0];
		A[0] = TT1;
		A[7] = A[6];
		A[6] = left_(A[5], 19);
		A[5] = A[4];
		A[4] = P0(TT2);
	}
	string b = "";
	for (int i = 0; i < 8; i++) {
		stringstream ss;
		ss << hex << A[i];
		string hexStr = ss.str();
		string paddedHex = string(8 - hexStr.length(), '0') + hexStr;
		b += paddedHex;
	}
	string c_str = XOR(iv, b);
	return c_str;
}

string SM3(const string& p,string iv) {
	string padded = pad(p);
	int num = padded.size() / 128;
	string B = "";
	for (int i = 0; i < num; i++) {
		B = padded.substr(i * 128, 128);
		iv = CF(iv, B);
	}
	return iv;
}

string generateRandomString(int length) {
	string characters = "0123456789abcdefghijklmnopqrstuvwxyz";
	random_device rd;
	mt19937 gen(rd());
	uniform_int_distribution<> dis(0, characters.length() - 1);
	string randomString;
	for (int i = 0; i < length; ++i) {
		randomString += characters[dis(gen)];
	}
	return randomString;
}

string Lengthattack(string h, int n) {
	string s,c,m="",p="";
	for (int i = 0; i < n; i++) {
		s += '6';
	}
	vector<string> a;
	s = pad(s);
	a = cut(s, 2);
	for (int i = 0; i < s.length() / 2; i++) {
		if (a[i] == "80")
			p = p + 'Ç';
		else
		    p = p + char(hexToDecimal(a[i]));
	}
	cout << "附加消息为" << "66666" << endl;
	p += "66666";
	string padded = pad(p);
	for (int i = 128; i < padded.length(); i++) {
		m = m + padded[i];
	}
	int num = m.size() / 128;
	string B = "";
	for (int i = 0; i < num; i++) {
		B = m.substr(i * 128, 128);
		h = CF(h, B);
	}
	return h;
}

int main() {
	string iv = "7380166f4914b2b9172442d7da8a0600a96f30bc163138aae38dee4db0fb0e4e";
	int n = 10;
	string h,m,d,e,f,g="";
	m = generateRandomString(n);
	cout << "消息：" << m<<endl;
	h = SM3(m, iv);
	cout << "其hash值为：" << h << endl;
	d = Lengthattack(h, n);
	cout << "进行长度攻击得：" << d << endl;
	vector<string> a;
	e = pad(m);
	a = cut(e, 2);
	for (int i = 0; i < e.length()/2; i++) {
		if (a[i] == "80")
			g = g + 'Ç';
		else
		    g = g + char(hexToDecimal(a[i]));
	}
	e = g + "66666";
	f = SM3(e, iv);
	cout << "消息+填充+附加消息的hash值为：" << f << endl;
}

// 运行程序: Ctrl + F5 或调试 >“开始执行(不调试)”菜单
// 调试程序: F5 或调试 >“开始调试”菜单

// 入门使用技巧: 
//   1. 使用解决方案资源管理器窗口添加/管理文件
//   2. 使用团队资源管理器窗口连接到源代码管理
//   3. 使用输出窗口查看生成输出和其他消息
//   4. 使用错误列表窗口查看错误
//   5. 转到“项目”>“添加新项”以创建新的代码文件，或转到“项目”>“添加现有项”以将现有代码文件添加到项目
//   6. 将来，若要再次打开此项目，请转到“文件”>“打开”>“项目”并选择 .sln 文件
