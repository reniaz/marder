import requests
import struct
from socket import create_connection, socket
from app.decode import bdecode, BValue
from app.classes import Client, Peer, Torrent

handshake_format = "!B19s8x20s20s"

def get_request_data(url, params) -> BValue:
    request_content = requests.get(url=url, params=params).content
    request_data = bdecode(request_content)

    assert(isinstance(request_data, dict))
    if b'failure reason' in request_data:
        raise ValueError(f"Failure reason: {request_data[b'failure reason'].decode('utf-8')}")

    if b'warning message' in request_data:
        print(f"Warning: {request_data[b'warning message'].decode('utf-8')}")

    return request_data

def get_peer_list(data) -> list[Peer]:
    peers = []
    if b'peers' in data:
        for peer in data[b'peers']:
            peers.append(Peer(ip=peer[b'ip'].decode('utf-8'), port=peer[b'port']))

    return peers

def create_tcp_connection(torrent: Torrent, client: Client, address: tuple[str, int], timeout=2):
    try:
        sock = create_connection(address, timeout=timeout)
        handshake = struct.pack(handshake_format, 19, b'BitTorrent protocol', torrent.info_hash_digest, client.peer_id)
        assert(len(handshake) == 68)
        sock.sendall(handshake)
        sock_data = sock.recv(68)
        if len(sock_data) == 68:
            return sock, sock_data
    except Exception as e:
        print(f"[-] Exception {e} for: <{address[0]}|{address[1]}>")
        return None

    return None

def validate_connection(sock: socket, sock_data: tuple):
    protocol_type = sock_data[0]
    protocol_name = sock_data[1]

    if protocol_type != 19:
        print(f"[-] protocol_type {protocol_type} doesn't match '19'\n[-] Closing connection!")
        sock.close()
        exit(3)

    if protocol_name != b'BitTorrent protocol':
        print(f"[-] protocol_name {protocol_name} doesn't match b'BitTorrent protocol'\n[-] Closing connection!")
        sock.close()
        exit(3)

def close_socks(socks: list[socket]):
    for sock in socks:
        sock.close()
