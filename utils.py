import socket
import random
from typing import Optional

HOST = "rick"
MAX_BYTES = 4096

ID_PREFIX = "identifier"
MIN_DYNAMIC_PORT, MAX_DYNAMIC_PORT = 49152, 65535

def get_identifier_or_raise_exception(data: str) -> str:
    identifier = get_identifier_from_data(data)
    if identifier is not None:
        return identifier
    raise ValueError("indentifier was not found in the provided data")

def decrypt_cesar_word(word: str, key: int) -> str:
    decoded_word = ""
    for char in word:
        offset = ord("A") if char.isupper() else ord("a")
        new_ascii = (ord(char) - offset + key) % 26 + offset
        decoded_word += chr(new_ascii)

    return decoded_word

def first_digit_index(data: str) -> Optional[int]:
    for i, c in enumerate(data):
        if c.isnumeric():
            return i

    return None

def get_identifier_from_data(data: str) -> Optional[str]:
    """ Returns the identifier. If ID_PREFIX is not in data then an exception is raised """
    idx = data.find(ID_PREFIX)
    if idx != -1:
        return data[idx + len(ID_PREFIX) + 1:data.index("\n")]
    return None

def read_until_end(socket: socket.socket) -> bytes:
    all_data = b""
    while True:
        data = socket.recv(MAX_BYTES)
        if not data:
            break

        all_data += data

    return all_data


def read_until(socket: socket.socket, delimiter, encoding: str = "utf-8") -> str:
    """ Reads until delimiter is found. If delimiter is None (the default), it
    will read until the remote host closes the connection """

    all_data = ""
    while True:
        data = socket.recv(MAX_BYTES)
        if not data:
            break
        all_data += data.decode(encoding)

        if delimiter and delimiter in all_data:
            return all_data

    return all_data

def try_bind_socket(socket: socket.socket, tries: int = 10) -> int:
    """ Tries to bind a random port to a socket. It is highly unlikely that a person has bound
    the same port that me but handling this situation makes my program more robust """

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
