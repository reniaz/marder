from dataclasses import dataclass, field
from random import choices
from string import ascii_letters, digits

def _make_peer_id() -> bytes:
    suffix = ''.join(choices(ascii_letters + digits, k=12))
    return b'-MA0001-' + suffix.encode('ascii')

@dataclass
class Client:
    peer_id: bytes = field(default_factory=_make_peer_id)
    port: int = 6881

@dataclass
class TorrentFile:
    length: int
    path: list[str]

@dataclass
class Torrent:
    announce: str # per BEP-12 this gets ignored when announce_list is present
    announce_list: list # supersedes announce (first url usually same as announce)
    name: str
    piece_length: str
    pieces: bytes
    files: list[TorrentFile]
    total_size: int
    info_hash_digest: bytes=b''
    info_hash_hex: str=""

@dataclass
class Magnet:
    info_hash: bytes
    display_name: str | None = None
    trackers: list[str] | None = None
    peers: list[str] | None = None

@dataclass
class Peer:
    ip: str
    port: int
