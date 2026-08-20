from socket import socket

def recv_exactly(sock: socket, n: int) -> bytes:
    buf = bytes(0)
    while len(buf) < n:
        buf = sock.recv(n - len(buf))

    return buf

def read_message(sock: socket) -> tuple[int, bytes]:
    read_bytes = recv_exactly(sock, 4)
    read_int = int.from_bytes(read_bytes, "big")

    if read_int == 0:
        print(f"[*] read_message -> keep alive")
        return bytes(0)

    actual_bytes = recv_exactly(sock, read_int)
    msg_id = actual_bytes[0]
    payload = actual_bytes[1:]

    print(f"[*] read_message -> {msg_id}:{actual_bytes}")

    return (msg_id, payload)
