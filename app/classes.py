from dataclasses import dataclass

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
    info_hash_digest: bytes=b''
    info_hash_hex: str=""
