
from socket import socket


def recv_exactly(sock: socket, n: int) -> bytes:
    buf = bytes(0)
    while len(buf) < n:
        recv = sock.recv(n - len(buf))
        if recv == b'':
            raise ValueError("[-] Peer closed connection!")
        print(f"[*] recv_exactly -> buf: {buf}")

    return buf

def read_message(sock: socket):
    read_bytes = recv_exactly(sock, 4)
    read_int = int.from_bytes(read_bytes, "big")

    actual_bytes = recv_exactly(sock, read_int)
