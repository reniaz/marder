import sys
import struct
from socket import socket
from app.connection import close_socks, create_tcp_connection, get_peer_list, get_request_data
from app.torrent import parse_torrent, read_torrent_file
from app.magnet import parse_magnet_url
from app.classes import Client

def main():
    if len(sys.argv) <= 1:
        print("usage: marder <torrent_file|magnet_url>")
        exit(1)

    query = {}
    client = Client()

    if sys.argv[1].startswith("magnet"):
        magnet = parse_magnet_url(sys.argv[1])
        print(magnet)
        return# Implement magnet downloading later on M13
    else:
        data = read_torrent_file(sys.argv[1])
        torrent = parse_torrent(data)
        query = {'info_hash': torrent.info_hash_digest, 'peer_id': client.peer_id, 'port': client.port, 'uploaded': 0, 'downloaded': 0, 'left': torrent.total_size, 'compact': 1, 'event': 'started'}


    data = get_request_data(torrent.announce_list[0][0], query)

    peers = get_peer_list(data)
    if isinstance(peers, bytes):
        raise NotImplementedError("Compact not yet implemented! (M10)")

    connected_peer = None
    sock_data = None
    for peer in peers:
        connection = create_tcp_connection(torrent, client, (peer.ip, peer.port))
        if isinstance(connection, tuple):
            connected_peer = connection[0]
            sock_data = connection[1]
    assert(isinstance(connected_peer, socket))

    print(f"[+] sock_data: {sock_data}")

    connected_peer.close()

if __name__ == "__main__":
    main()

