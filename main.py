import sys
import requests
from app.decode import BValue, bdecode
from app.torrent import parse_torrent, read_torrent_file
from app.magnet import parse_magnet_url
from app.classes import Client, Peer

def main():
    if len(sys.argv) <= 1:
        print("usage: marder <torrent_file|magnet_url>")
        exit(1)

    query = {}
    client = Client()

    if sys.argv[1].startswith("magnet"):
        magnet = parse_magnet_url(sys.argv[1])
        pass # Implement magnet downloading later on M13
    else:
        data = read_torrent_file(sys.argv[1])
        torrent = parse_torrent(data)
        query = {'info_hash': torrent.info_hash_digest, 'peer_id': client.peer_id, 'port': client.port, 'uploaded': 0, 'downloaded': 0, 'left': torrent.total_size, 'compact': 1, 'event': 'started'}

    data = get_request_data(torrent.announce_list[0][0], query)

    peers = get_peer_list(data)
    if isinstance(peers, bytes):
        raise NotImplementedError("Compact not yet implemented! (M10)")

def get_request_data(url, params) -> BValue:
    request_content = requests.get(url=url, params=params).content
    request_data = bdecode(request_content)

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

if __name__ == "__main__":
    main()

