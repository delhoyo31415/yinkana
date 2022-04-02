import socket

import utils


def first(identifier: str) -> str:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((utils.HOST, 2000))
        print(sock.recv(utils.MAX_BYTES).decode())
        sock.sendall(identifier.encode())

        data = utils.read_until_finish(sock)
        print(data)
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

all_challenges = [first, second]
