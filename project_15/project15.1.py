from Crypto.Util.number import inverse
import socket
from random import randint

# Parameter Configuration
PRIME = 0xFFFFFFFEFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF00000000FFFFFFFFFFFFFFFF
ORDER = 0xFFFFFFFEFFFFFFFFFFFFFFFFFFFFFFFF7203DF6B21C6052B53BBF40939D54123
COEFFICIENT_A = 0xFFFFFFFEFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF00000000FFFFFFFFFFFFFFFC
COEFFICIENT_B = 0x28E9FA9E9D9F5E344D5A9E4BCF6509A7F39789F515AB8F92DDBCBD414D940E93
BASE_POINT_X = 0x421DEBD61B62EAB6746434EBC3CC315E32220B3BADD50BDC4C4E6C147FEDD43D
BASE_POINT_Y = 0xBC3736A2F4F6779C59BDCEE36B692153D0A9877CC62A474002DF32E52139F0A0
BASE_POINT = (BASE_POINT_X, BASE_POINT_Y)


def add_points(point1, point2):
    if point1 == 0 and point2 == 0: return 0
    elif point1 == 0: return point2
    elif point2 == 0: return point1
    else:
        if point1[0] > point2[0]:
            point1, point2 = point2, point1
        slope_ratio = (point2[1] - point1[1])*inverse(point2[0] - point1[0], PRIME) % PRIME

        res_point = [(slope_ratio**2 - point1[0] - point2[0]) % PRIME]
        res_point.append((slope_ratio*(point1[0] - res_point[0]) - point1[1]) % PRIME)

        return (res_point[0], res_point[1])

def double_point(point):
    slope_ratio = (3*point[0]**2 + COEFFICIENT_A)*inverse(2*point[1], PRIME) % PRIME

    res_point = [(slope_ratio**2 - 2*point[0]) % PRIME]
    res_point.append((slope_ratio*(point[0] - res_point[0]) - point[1])%PRIME)

    return (res_point[0], res_point[1])

def multiply_point(coefficient, point):
    duplicate = point
    res_point = 0
    binary_coefficient = bin(coefficient)[2:]
    num_digits = len(binary_coefficient)
    for i in reversed(range(num_digits)):
        if binary_coefficient[i] == '1':
            res_point = add_points(res_point, duplicate)
        duplicate = double_point(duplicate)

    return res_point


client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client_socket.bind(('', 11111))

print("等待链接中……")


private_key = randint(1,ORDER-1)
x_coord, source_address = client_socket.recvfrom(1024)
x_coord = int(x_coord.decode(),16)
y_coord, source_address = client_socket.recvfrom(1024)
y_coord = int(y_coord.decode(),16)
public_key_point = (x_coord, y_coord)
public_key_point = multiply_point(inverse(private_key, PRIME), public_key_point)
public_key_point = add_points(public_key_point, (BASE_POINT_X, -BASE_POINT_Y))


x_coord, source_address = client_socket.recvfrom(1024)
x_coord = int(x_coord.decode(),16)
y_coord, source_address = client_socket.recvfrom(1024)
y_coord = int(y_coord.decode(),16)
first_point = (x_coord, y_coord)
message, source_address = client_socket.recvfrom(1024)
message = int(message.decode(),16)
first_constant = randint(1,ORDER-1)
second_constant = randint(1,ORDER-1)
second_point = multiply_point(first_constant, BASE_POINT)
temp_x1, temp_y1 = multiply_point(second_constant, first_point)
temp_x1, temp_y1 = add_points((temp_x1, temp_y1), second_point)
response =(temp_x1 + message) % ORDER
second_response = (private_key * second_constant) % ORDER
third_response = (private_key * (response+first_constant)) % ORDER

client_socket.sendto(hex(response).encode(), source_address)
client_socket.sendto(hex(second_response).encode(), source_address)
client_socket.sendto(hex(third_response).encode(), source_address)

print("链接关闭")
