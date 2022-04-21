import struct
import array
import base64
import sys

import dataclasses
from dataclasses import dataclass

HEADER_LEN = 10
HEADER_FORMAT = "!3sHB2H"


# Obtained from: https://bitbucket.org/DavidVilla/inet-checksum/src/master/inet_checksum.py
def calculate_checksum(raw: bytes) -> int:
    if len(raw) % 2 == 1:
        raw += b'\0'

    s = sum(array.array('H', raw))
    s = (s >> 16) + (s & 0xffff)
    s += s >> 16
    s = ~s

    if sys.byteorder == 'little':
        s = ((s >> 8) & 0xff) | s << 8

    return s & 0xffff


@dataclass
class YAPHeader:
    magic_number: bytes
    msg_type: int
    code: int
    checksum: int
    sequence: int

    def serialize(self) -> bytes:
        return struct.pack(HEADER_FORMAT, *dataclasses.astuple(self))

@dataclass
class YAPPacket:
    header: YAPHeader
    payload: bytes

    def serialize(self) -> bytes:
        return self.header.serialize() + base64.b64encode(self.payload)

def build_yap_packet(*, msg_type: int, code: int, sequence: int, payload: bytes) -> YAPPacket:
    header = YAPHeader(b"YAP", msg_type, code, 0, sequence)
    packet = YAPPacket(header, payload)
    header.checksum = calculate_checksum(packet.serialize())

    return packet

def to_yap_packet(raw: bytes) -> YAPPacket:
    if len(raw) < HEADER_LEN:
        raise ValueError(f"Packet must have at least {HEADER_LEN} bytes")

    header = YAPHeader(*struct.unpack(HEADER_FORMAT, raw[:HEADER_LEN]))
    payload = base64.b64decode(raw[HEADER_LEN:])

    return YAPPacket(header, payload)


def make_yap_request(*, sequence: int, payload: bytes) -> YAPPacket:
    return build_yap_packet(msg_type=0, code=0, sequence=sequence, payload=payload)
