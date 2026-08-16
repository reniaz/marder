import sys
from app.decode import bdecode, get_info_indexes
from app.classes import Torrent, TorrentFile
from hashlib import sha1
from app.magnet import parse_magnet_url

def read_test_file(path) -> bytes:
    with open(path, mode='rb') as f:
        data = f.read()

    return data

def parse_torrent(raw: bytes) -> Torrent:
    data = bdecode(raw)
    assert(isinstance(data, dict))
    info = data[b'info']
    assert(isinstance(info, dict))

    start, end = get_info_indexes(raw)
    info_hash = sha1(raw[start:end])

    if b'files' in info:
        files = [TorrentFile(length = f[b'length'], path = [p.decode('utf-8') for p in f[b'path']]) for f in info[b'files']]
    else:
        files = [TorrentFile(length = info[b'length'], path = [info[b'name'].decode('utf-8')])]

    announce_list = [[url.decode('utf-8') for url in url_list] for url_list in data[b'announce-list']]

    return Torrent(announce=data[b'announce'].decode('utf-8'),
                   announce_list=announce_list,
                   name=info[b'name'].decode('utf-8'),
                   piece_length=info[b'piece length'],
                   pieces=info[b'pieces'],
                   files=files,
                   info_hash_digest=info_hash.digest(),
                   info_hash_hex=info_hash.hexdigest())

def main():
    if len(sys.argv) <= 1:
        print("usage: marder <torrent_file|magnet_url>")
        exit(1)

    if sys.argv[1].startswith("magnet"):
        parse_magnet_url(sys.argv[1])
    else:
        data = read_test_file(sys.argv[1])
        # print("Data: " + str(data))
        torrent = parse_torrent(data)
        print(torrent)

if __name__ == "__main__":
    main()

