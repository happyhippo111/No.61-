# main2.py
from sm2 import *
import socket
import sys
from random import randint
import binascii
from gmssl import sm3,func

def establish_connection(address=('127.0.0.1', 111)):
    client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    address = ('127.0.0.1', 1112)
    client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    try:
        client.connect(('127.0.0.1', 1112))
        print("连接建立")
    except Exception:
        print('连接失败')
        sys.exit()
    else:
        # step 1
        d1 = randint(1, N - 1)
        P1 = ECC_mul(inverse(d1, P), G)
        x, y = hex(P1[0]), hex(P1[1])

        client.sendto(x.encode('utf-8'), address)
        client.sendto(y.encode('utf-8'), address)

        # step 3
        msg = "hello !!!"
        msg = hex(int(binascii.b2a_hex(msg.encode()).decode(), 16)).upper()[2:]

        Z = sm3.sm3_hash(func.bytes_to_list(msg.encode()))
        M = Z + msg
        e = sm3.sm3_hash(func.bytes_to_list(M.encode()))
        k1 = randint(1, N - 1)
        Q1 = ECC_mul(k1, G)
        x, y = hex(Q1[0]), hex(Q1[1])

        client.sendto(x.encode('utf-8'), address)
        client.sendto(y.encode('utf-8'), address)
        client.sendto(e.encode('utf-8'), address)

        # step 5
        r, _ = client.recvfrom(1024)
        r = int(r.decode(), 16)
        s2, _ = client.recvfrom(1024)
        s2 = int(s2.decode(), 16)
        s3, _ = client.recvfrom(1024)
        s3 = int(s3.decode(), 16)
        s = ((d1 * k1) * s2 + d1 * s3 - r) % N
        print(f"Signature : {hex(r)} {hex(s)}")
        client.close()
