import socket
import hashlib
from typing import Optional

import utils
import yap


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

def fifth(identifier: str) -> str:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((utils.HOST, 9003))
        sock.sendall(identifier.encode())

        # TODO: make this more robust
        first_part = sock.recv(utils.MAX_BYTES)
        colon_index = first_part.index(b":")
        remaining_data = int(first_part[:colon_index].decode()) - (len(first_part) - colon_index - 1)
        sha1 = hashlib.sha1(first_part[colon_index + 1:])

        while remaining_data != 0:
            data = sock.recv(min(utils.MAX_BYTES, remaining_data))
            sha1.update(data)
            remaining_data -= len(data)

        sock.sendall(sha1.digest())
        last_data = utils.read_until(sock)

        print(last_data)
        return utils.get_identifier_from_data(last_data)

def sixth(identifier: str) -> str:
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        packet = yap.make_yap_request(sequence=1, payload=identifier.encode())
        sock.sendto(packet.serialize(), ("rick", 6001))
        raw_recieve = sock.recvfrom(utils.MAX_BYTES)[0]
        msg = yap.to_yap_packet(raw_recieve).payload.decode()

        print(msg)
        return utils.get_identifier_from_data(msg)

all_challenges = [first, second, third, fourth, fifth, sixth]
