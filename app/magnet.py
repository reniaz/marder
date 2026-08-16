from urllib.parse import parse_qs, urlparse
from app.classes import Magnet
from base64 import b32decode

def parse_magnet_url(url: str) -> Magnet:
    data = parse_qs(urlparse(url).query)
    info_hash_raw = data['xt'][0]

    if info_hash_raw.startswith("urn:btih:"):
        info_hash = _remove_prefix(info_hash_raw)
        if len(info_hash) == 32:
            info_hash = b32decode(info_hash, casefold=True)
        elif len(info_hash) == 40:
            info_hash = bytes.fromhex(info_hash)
        else:
            raise ValueError("non-hexadecimal number found in hash")
    else:
        raise ValueError("Only v1 Torrents are supported!")

    url_list = data.get('tr', None)

    display_name = None
    if 'dn' in data:
        display_name = data['dn'][0]

    peers = data.get('x.pe', None)

    return Magnet(info_hash=info_hash, display_name=display_name, trackers=url_list, peers=peers)

def _remove_prefix(raw_info_hash: str):
    to_slice = len("urn:btih:")
    return raw_info_hash[to_slice:]
