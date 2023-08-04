from sm2 import *
import socket
import sys
from random import randint
import binascii
from gmssl import sm3,func

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
    client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    client.bind(('', 12321))

    print("等待建立连接...")

    # step 2------------------------------------------

    d2 = randint(1, N - 1)
    x, address = client.recvfrom(1024)
    x = int(x.decode(), 16)
    y, address = client.recvfrom(1024)
    y = int(y.decode(), 16)
    P1 = (x, y)
    P1 = ECC_mul(inverse(d2, P), P1)
    P1 = Point_Add(P1, (G_X, -G_Y))

    # step 4------------------------------------------
    x, address = client.recvfrom(1024)
    x = int(x.decode(), 16)
    y, address = client.recvfrom(1024)
    y = int(y.decode(), 16)
    Q1 = (x, y)
    e, address = client.recvfrom(1024)
    e = int(e.decode(), 16)
    k2 = randint(1, N - 1)
    k3 = randint(1, N - 1)
    Q2 = ECC_mul(k2, G)
    (x1, y1)= ECC_mul(k3, Q1)
    (x1, y1)= Point_Add((x1, y1), Q2)
    r = (x1 + e) % N
    s2 = (d2 * k3) % N
    s3 = (d2 * (r + k2)) % N
    client.sendto(hex(r).encode(), address)
    client.sendto(hex(s2).encode(), address)
    client.sendto(hex(s3).encode(), address)
    print("连接已关闭")


main1()
