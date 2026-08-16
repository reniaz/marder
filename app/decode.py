
BValue = int | bytes | list["BValue"] | dict[bytes, "BValue"]

def bdecode(data) -> BValue:
    '''Main function to decode bencoded data'''
    value, i = _decode(data, 0)
    if i != len(data):
        raise ValueError(f"trailing bytes at {i}")
    return value

def _skip(data, i) -> int:
    if i >= len(data):
        raise ValueError(f"unexpected end of data at {i}")

    if data[i:i+1] == b'd':
        i += 1
        while data[i:i+1] != b'e':
            i = _skip(data, i)
        return i + 1
    elif data[i:i+1] == b'l':
        i += 1
        while data[i:i+1] != b'e':
            i = _skip(data, i)
        return i + 1
    elif data[i:i+1] == b'i':
        return data.index(b'e', i) + 1
    elif data[i:i+1].isdigit():
        colon = data.index(b':', i)
        n = int(data[i:colon])
        start = colon + 1
        return start + n
    else:
        raise ValueError(f"no branch matched {data[i:i+1]!r} at {i}")

def get_info_indexes(data, i=0) -> tuple[int, int]:
    if data[i:i+1] == b'd':
        i += 1
        key_bytes, next_i = _decode(data, i)

        while key_bytes != b'info' and next_i < len(data):
            next_i = _skip(data, next_i)
            key_bytes, next_i = _decode(data, next_i)

        if key_bytes != b'info':
            raise ValueError("b'info' not found!")

        start = next_i
        i = _skip(data, next_i)
        return start, i
    else:
        raise ValueError(f"no branch matched {data[i:i+1]!r} at {i}")

def _decode(data, i=0) -> tuple[BValue, int]:
    if i >= len(data):
        raise ValueError(f"unexpected end of data at {i}")

    if data[i:i+1] == b'd':
        hash = {}
        i += 1
        while data[i:i+1] != b'e':
            key, i = _decode(data, i)
            hash[key], i = _decode(data, i)
        return hash, i + 1
    elif data[i:i+1] == b'l':
        i += 1
        elist = []
        while data[i:i+1] != b'e':
            value, i = _decode(data, i)
            elist.append(value)
        return elist, i + 1
    elif data[i:i+1] == b'i':
        i += 1
        end = i
        while data[end:end+1] != b'e' and end < len(data):
            end += 1
        return int(data[i:end]), end+1
    elif data[i:i+1].isdigit():
        colon = data.index(b':', i)
        n = int(data[i:colon])
        start = colon + 1
        return data[start:start+n], start + n
    else:
        raise ValueError(f"no branch matched {data[i:i+1]!r} at {i}")
