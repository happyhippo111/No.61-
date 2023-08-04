# main1.py
from sm2 import *
import socket
import sys
from random import randint
import binascii

def establish_connection(address=('127.0.0.1', 111)):
    client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        client.connect(address)
        print("连接建立")
        return client
    except Exception:
        print('连接失败')
        sys.exit()


def main1():
    client = establish_connection()
    address = ('127.0.0.1', 111)

    # step1
    d1 = randint(1, N - 1)
    d2 = randint(1, N - 1)
    # step2
    # Encrypt:
    k = randint(1, N - 1)
    C_1 = ECC_mul(k, G)
    P_K = ECC_mul(inverse(d1 * d2, P) - 1, G)  # public key
    G_2 = ECC_mul(k, P_K)
    t = KDF('{:064X}'.format(G_2[0]) + '{:064X}'.format(G_2[1]), 64)
    msg = "hello"
    msg = hex(int(binascii.b2a_hex(msg.encode()).decode(), 16)).upper()[2:]
    print(msg)
    C_2 = hex(int(msg, 16) ^ int(t, 2))[2:].upper()
    C_3 = sm3.sm3_hash(list(bytes.fromhex('{:064X}'.format(G_2[0]) + msg + '{:064X}'.format(G_2[1]))))

    # step2
    C = str(C_1[0]) + str(C_1[1]) + C_2 + C_3
    if C_1 != 0:
        T1 = ECC_mul(inverse(d1, P), C_1)
        x, y = hex(T1[0]), hex(T1[1])
        client.sendto(x.encode('utf-8'), address)
        client.sendto(y.encode('utf-8'), address)

    x2, address = client.recvfrom(1024)
    x2 = int(x2.decode(), 16)
    y2, address = client.recvfrom(1024)
    y2 = int(y2.decode(), 16)

    T2 = (x2, y2)

    # step4
    T2 = ECC_mul(inverse(d2, P), T1)
    G_3 = Point_Add(T2, (C_1[0], -C_1[1]))
    t = KDF('{:064X}'.format(G_2[0]) + '{:064X}'.format(G_2[1]), 64)
    M = hex(int(C_2, 16) ^ int(t, 2))[2:].upper()
    print(M)


main1()