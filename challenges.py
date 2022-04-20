import socket
from typing import Optional

import utils


def first(identifier: str) -> str:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((utils.HOST, 2000))
        print(sock.recv(utils.MAX_BYTES).decode())
        sock.sendall(identifier.encode())

        data = utils.read_until(sock)
        return utils.get_identifier_from_data(data)


def second(identifier: str) -> str:
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        port = utils.try_bind_socket(sock)
        sock.sendto(f"{port} {identifier}".encode(), (utils.HOST, 4000))
        data, addr = sock.recvfrom(utils.MAX_BYTES)
        print(data.decode())

        sock.sendto(identifier.upper().encode(), addr)
        data = sock.recvfrom(utils.MAX_BYTES)[0].decode()
        print(data)
        return utils.get_identifier_from_data(data)

def third(identifier: str) -> str:
    end_delimiter = "that's the end"

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((utils.HOST, 3002))
        large_text = utils.read_until(sock, end_delimiter)
        words = len(large_text[:large_text.index(end_delimiter)].split())

        sock.sendall(f"{identifier} {words}".encode())
        remaining_data = utils.read_until(sock)

        print(remaining_data)
        return utils.get_identifier_from_data(remaining_data)

def fourth(identifier: str) -> str:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((utils.HOST, 6501))

        all_data = ""
        index: Optional[int] = None

        while index is None:
            data = sock.recv(utils.MAX_BYTES)
            all_data += data.decode()
            index = utils.first_digit_index(all_data)

        key = int(all_data[index])
        decoded_msg = " ".join([utils.decrypt_cesar_word(word, key) for word in all_data[:index].split()[-key:]])

        sock.sendall(f"{identifier} {decoded_msg} --".encode())

        remaining_data = utils.read_until(sock)

        print(remaining_data)
        return utils.get_identifier_from_data(remaining_data)

all_challenges = [first, second, third, fourth]
