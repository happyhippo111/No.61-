from sm2 import *
import socket
import sys
from random import randint

def establish_connection(address=('127.0.0.1', 111)):
    client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        client.bind(address)
        print("连接建立")
        return client
    except Exception as e:
        print('连接失败:', e)
        sys.exit()

def main2():
    client = establish_connection(('', 111))
    print("等待建立连接...")

    # step1
    d2 = randint(1, N - 1)

    # STEP3
    x, address = client.recvfrom(1024)
    x = int(x.decode(), 16)
    y, address = client.recvfrom(1024)
    y = int(y.decode(), 16)

    T1 = (x, y)

    # step4
    T2 = ECC_mul(inverse(d2, P), T1)
    x2, y2 = hex(T1[0]), hex(T1[1])
    client.sendto(x2.encode('utf-8'), address)
    client.sendto(y2.encode('utf-8'), address)
    print("连接已关闭")
