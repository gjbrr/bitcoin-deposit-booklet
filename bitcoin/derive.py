import base58
import hashlib

from bip32 import BIP32
from bitcoin.segwit_addr import encode as bech32_encode


# ---------- DERIVE ADDRESSES ----------
_zpub_MAINNET_VERSION = bytes.fromhex("0488b21e")

def normalize_to_xpub(key):
    """
    Accepts zpub/ypub/zpub (mainnet account-level extended PUBLIC keys) and
    normalizes to standard 'zpub' version bytes so BIP32.from_zpub() can parse
    it. This only rewrites the 4-byte SLIP-132 version prefix -- the actual
    key material (depth, fingerprint, chain code, public key) is untouched,
    so the derived addresses are identical to what the original prefix
    (e.g. zpub) represents. Purely a public-key/encoding operation -- no
    private key material is ever involved.
    """
    key = "".join(key.split())
    raw = base58.b58decode_check(key)
    if len(raw) != 78:
        raise ValueError(f"Not a valid extended key (unexpected length {len(raw)})")
    version = raw[:4]
    _KNOWN_PRIVATE_VERSIONS = {
        bytes.fromhex("0488ade4"),  # xprv
        bytes.fromhex("049d7878"),  # yprv
        bytes.fromhex("04b2430c"),  # zprv
    }
    if version in _KNOWN_PRIVATE_VERSIONS or raw[45] not in (0x02, 0x03):
        raise ValueError(
            "This looks like a PRIVATE extended key (prv), not a public one (pub) -- "
            "refusing to use it. Double check you copied the PUBLIC key."
        )
    normalized = _zpub_MAINNET_VERSION + raw[4:]
    return base58.b58encode_check(normalized).decode()

def hash160(b):
    return hashlib.new('ripemd160', hashlib.sha256(b).digest()).digest()

def derive_addresses(zpub, n):
    xpub = normalize_to_xpub(zpub)
    b32 = BIP32.from_xpub(xpub)
    addrs = []
    for i in range(n):
        pubkey = b32.get_pubkey_from_path(f"m/0/{i}")
        h = hash160(pubkey)
        addr = bech32_encode("bc", 0, h)
        addrs.append(addr)
    return addrs
