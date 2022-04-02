import socket
import random

HOST = "rick"
MAX_BYTES = 4096

ID_OFFSET = len("identifier:")
MIN_DYNAMIC_PORT, MAX_DYNAMIC_PORT = 49152, 65535

def get_identifier_from_data(data: str) -> str:
    return data[ID_OFFSET:data.index("\n")]

def read_until_finish(socket: socket.socket) -> str:
    all_data = ""
    while True:
        data = socket.recv(MAX_BYTES)
        if not data:
            break
        all_data += data.decode()

    return all_data

def try_bind_socket(socket: socket.socket, tries: int = 10) -> int:
    rand_port = 0

    while tries > 0:
        try:
            rand_port = random.randint(MIN_DYNAMIC_PORT, MAX_DYNAMIC_PORT)
            socket.bind(("", rand_port))
            break
        except OSError:
            tries -= 1

    if tries == 0:
        raise OSError
    return rand_port
