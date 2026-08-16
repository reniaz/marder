from urllib.parse import parse_qs, urlparse

def parse_magnet_url(url: str):
    data = parse_qs(urlparse(url).query)
    info_hash_raw = data['xt'][0]

    if info_hash_raw.startswith("urn:btih:"):
        info_hash = info_hash_raw[9:]
    elif info_hash_raw.startswith("urn:btmh:"):
        info_hash = info_hash_raw[9:]
    else:
        info_hash = info_hash_raw

    print(info_hash)
