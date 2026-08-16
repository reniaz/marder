from app.decode import bdecode, get_info_indexes
from app.classes import Torrent, TorrentFile
from hashlib import sha1

def read_torrent_file(path) -> bytes:
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

    total_size = sum(f.length for f in files)

    return Torrent(announce=data[b'announce'].decode('utf-8'),
                   announce_list=announce_list,
                   name=info[b'name'].decode('utf-8'),
                   piece_length=info[b'piece length'],
                   pieces=info[b'pieces'],
                   files=files,
                   total_size=total_size,
                   info_hash_digest=info_hash.digest(),
                   info_hash_hex=info_hash.hexdigest())
