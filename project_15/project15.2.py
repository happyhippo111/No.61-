from gmssl import sm3, func
from Crypto.Util.number import inverse
import socket
import sys
import binascii
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
    if point1 == 0 and point2 == 0:
        return 0
    elif point1 == 0:
        return point2
    elif point2 == 0:
        return point1
    else:
        if point1[0] > point2[0]:
            point1, point2 = point2, point1
        slope_ratio = (point2[1] - point1[1]) * inverse(point2[0] - point1[0], PRIME) % PRIME

        res_point = [(slope_ratio ** 2 - point1[0] - point2[0]) % PRIME]
        res_point.append((slope_ratio * (point1[0] - res_point[0]) - point1[1]) % PRIME)

        return (res_point[0], res_point[1])


def double_point(point):
    slope_ratio = (3 * point[0] ** 2 + COEFFICIENT_A) * inverse(2 * point[1], PRIME) % PRIME

    res_point = [(slope_ratio ** 2 - 2 * point[0]) % PRIME]
    res_point.append((slope_ratio * (point[0] - res_point[0]) - point[1]) % PRIME)

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


address = ('127.0.0.1', 11111)
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

try:
    client_socket.connect(('127.0.0.1', 11111))
    print("Connection established")
except Exception:
    print('Connection failed')
    sys.exit()
else:
    # Step One------------------------------------------
    private_key = randint(1, ORDER - 1)
    public_key_point = multiply_point(inverse(private_key, PRIME), BASE_POINT)
    x_coord, y_coord = hex(public_key_point[0]), hex(public_key_point[1])

    client_socket.sendto(x_coord.encode('utf-8'), address)
    client_socket.sendto(y_coord.encode('utf-8'), address)

    # Step Three------------------------------------------
    raw_message = "SM2 2P sign with real network communication"
    encoded_message = hex(int(binascii.b2a_hex(raw_message.encode()).decode(), 16)).upper()[2:]
    user_id = "WTYTW"
    encoded_user_id = hex(int(binascii.b2a_hex(user_id.encode()).decode(), 16)).upper()[2:]
    uid_length = '{:04X}'.format(len(encoded_user_id) * 4)
    indicative_user_id = uid_length + encoded_user_id + '{:064X}'.format(COEFFICIENT_A) + '{:064X}'.format(COEFFICIENT_B) + '{:064X}'.format(BASE_POINT_X) + '{:064X}'.format(BASE_POINT_Y)

    z_val = sm3.sm3_hash(func.bytes_to_list(indicative_user_id.encode()))
    combined_message = z_val + encoded_message
    message_hash = sm3.sm3_hash(func.bytes_to_list(combined_message.encode()))
    first_rand_num = randint(1, ORDER - 1)
    first_point = multiply_point(first_rand_num, BASE_POINT)
    x_coord, y_coord = hex(first_point[0]), hex(first_point[1])

    client_socket.sendto(x_coord.encode('utf-8'), address)
    client_socket.sendto(y_coord.encode('utf-8'), address)
    client_socket.sendto(message_hash.encode('utf-8'), address)

    # Step Five------------------------------------------
    response_value, _ = client_socket.recvfrom(1024)
    response_value = int(response_value.decode(), 16)
    first_response, _ = client_socket.recvfrom(1024)
    first_response = int(first_response.decode(), 16)
    second_response, _ = client_socket.recvfrom(1024)
    second_response = int(second_response.decode(), 16)
    final_response = ((private_key * first_rand_num) * first_response + private_key * second_response - response_value) % ORDER
    print(f"Signature : {hex(response_value)} {hex(final_response)}")
    client_socket.close()