<div align="center">

# 🦡 Marder

**A BitTorrent client written from scratch in Python.**

No `libtorrent`. No `bencodepy`. Just the spec and a byte cursor.

[![Python](https://img.shields.io/badge/python-3.12%2B-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![Status](https://img.shields.io/badge/status-work%20in%20progress-orange)]()
[![Progress](https://img.shields.io/badge/milestones-2%20%2F%2013-blue)]()
[![Dependencies](https://img.shields.io/badge/dependencies-none-brightgreen)]()

</div>

---

Named after the marten — small, fast, and notorious for chewing things into pieces.

## Why

The BitTorrent protocol is a rare thing: a real, widely-deployed distributed system whose core specification fits on a few pages. Building a client from the spec upward means writing a recursive-descent parser, a binary wire protocol, a concurrent scheduler, and a peer-selection strategy — all of which transfer well beyond torrents.

Nothing here is meant to compete with qBittorrent. It's meant to be understood.

## Roadmap

- [x] **M1** — Bencode decoder
- [x] **M2** — Metadata parsing + infohash
- [x] **M3** — Magnet URI parsing &nbsp;·&nbsp; *in progress*
- [x] **M4** — HTTP tracker announce
- [ ] **M5** — Peer handshake
- [ ] **M6** — Download a single piece
- [ ] **M7** — Full single-file download
- [ ] **M8** — Concurrent peers (`asyncio`)
- [ ] **M9** — Multi-file torrents
- [ ] **M10** — UDP trackers ([BEP 15](https://www.bittorrent.org/beps/bep_0015.html))
- [ ] **M11** — Terminal UI
- [ ] **M12** — Uploading / seeding
- [ ] **M13+** — Metadata exchange, DHT, PEX

> [!NOTE]
> Metadata parsing works end to end. Nothing touches the network yet.

## Usage

```python
data    = read_test_file()
torrent = parse_torrent(data)

torrent.name           # 'test_folder'
torrent.piece_length   # 32768
torrent.info_hash      # b'\xd2GN\x86...'  — 20 raw bytes
torrent.files          # [TorrentFile(length=17614527, path=['images', '…jpg']), …]
```

Info hash verified against qBittorrent.

## Design notes

<details>
<summary><b>Everything is bytes until proven otherwise</b></summary>

<br>

Bencode strings are byte strings, not text. `pieces` is a concatenation of raw SHA-1 digests and will not survive a UTF-8 round trip — `chr()` and early `.decode()` calls silently inflate every byte above `0x7F` and corrupt the hash.

Fields are decoded to `str` individually, at the point where they're known to be text (`announce`, `name`, `path` components), and nowhere else.

</details>

<details>
<summary><b>The infohash is taken from the original file bytes</b></summary>

<br>

Not from a re-encoding of the decoded dict. A separate skip-only pass records the byte span of the `info` value, and SHA-1 runs over that raw slice.

Re-encoding would risk producing bytes that differ from whatever tool created the torrent — different key ordering, different integer form — yielding a hash no tracker recognises, with no error to explain why.

</details>

<details>
<summary><b>Two parsers over the same grammar</b></summary>

<br>

`_decode` builds values; `_skip` only computes lengths. They must agree exactly, so both run against the same corpus under the invariant:

```python
assert _skip(x, 0) == len(x)
```

A `_skip` that quietly disagrees with `_decode` is precisely how you get a wrong infohash and no diagnostic.

</details>

<details>
<summary><b>A typed boundary</b></summary>

<br>

Bencode decodes to a recursive union — `int | bytes | list | dict` — which is honest but miserable to carry through a program. `parse_torrent` converts once into dataclasses; everything downstream works with real types.

Single-file and multi-file torrents are normalised to the same shape, so the piece-offset arithmetic in M9 has one case to handle instead of two.

</details>

## Layout

```
bencode.py    _decode, _skip, get_info_indexes
torrent.py    Torrent / TorrentFile dataclasses, parse_torrent
```

## Testing

Decoder correctness rests on a hand-written corpus covering each type, the empty forms (`le`, `de`, `0:`), nesting, multi-digit string lengths, and negative integers — plus malformed input that must **raise rather than hang**: truncated values, trailing bytes, unknown type bytes.

> [!TIP]
> Debian and Ubuntu ISOs, or anything from the Internet Archive, make good integration targets — legal, well-seeded, and they publish checksums, which is exactly what M7 needs to verify against.

## References

| Spec | Covers |
|:--|:--|
| [BEP 3](https://www.bittorrent.org/beps/bep_0003.html) | Core protocol — bencoding, metainfo, trackers, peer wire |
| [BEP 12](https://www.bittorrent.org/beps/bep_0012.html) | Multitracker — `announce-list` tier semantics |
| [BEP 15](https://www.bittorrent.org/beps/bep_0015.html) | UDP tracker protocol |
| [BEP 9](https://www.bittorrent.org/beps/bep_0009.html) · [BEP 10](https://www.bittorrent.org/beps/bep_0010.html) | Metadata exchange for magnet links |
| [BEP 5](https://www.bittorrent.org/beps/bep_0005.html) | DHT |
| [theory.org](https://wiki.theory.org/BitTorrentSpecification) | Unofficial spec — more detailed than BEP 3 on the wire protocol |

## Licence

Not yet chosen.
