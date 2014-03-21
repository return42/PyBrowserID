# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.
"""

Utilities for dealing with Signed JSON Web Tokens.

"""

import hashlib

from browserid.crypto import Key, DSKey, RSKey  # NOQA

from browserid.utils import decode_bytes, encode_bytes
from browserid.utils import decode_json_bytes, encode_json_bytes


def parse(jwt):
    """Parse a JWT from a string."""
    header, payload, signature = jwt.split(".")
    signed_data = header + "." + payload
    try:
        algorithm = decode_json_bytes(header)["alg"]
    except KeyError:
        raise ValueError("badly formed JWT")
    payload = decode_json_bytes(payload)
    signature = decode_bytes(signature)
    return JWT(algorithm, payload, signature, signed_data)


def generate(payload, key):
    """Generate and sign a JWT for a dict payload."""
    alg = key.__class__.__name__[:-3]
    header = encode_json_bytes({"alg": alg})
    payload = encode_json_bytes(payload)
    signed_data = ".".join((header, payload)).encode("ascii")
    signature = encode_bytes(key.sign(signed_data))
    return ".".join((header, payload, signature))


class JWT(object):
    """Class for parsing signed JSON Web Tokens.

    To parse a JWT from a bytestring, use the module-level parse() function.
    This class is really only for internal purposes.
    """

    def __init__(self, algorithm, payload, signature, signed_data):
        self.algorithm = algorithm
        self.payload = payload
        self.signature = signature
        self.signed_data = signed_data

    def check_signature(self, key_data):
        """Check that the JWT was signed with the given key."""
        # Legacy BrowserID uses "algorithm" field, while latest
        # JWT spec uses "kty", and they have different formats.
        try:
            kty = key_data["kty"][:2]
        except KeyError:
            kty = key_data["algorithm"]
        if not self.algorithm.startswith(kty):
            return False
        key = load_key(self.algorithm, key_data)
        return key.verify(self.signed_data.encode("ascii"), self.signature)


def load_key(algorithm, key_data):
    """Load a Key object from the given data."""
    if not algorithm.isalnum():
        msg = "unknown signing algorithm: %s" % (algorithm,)
        raise ValueError(msg)
    try:
        key_class = globals()[algorithm + "Key"]
    except KeyError:
        msg = "unknown signing algorithm: %s" % (algorithm,)
        raise ValueError(msg)
    return key_class(key_data)


class RS64Key(RSKey):
    DIGESTSIZE = 256
    HASHNAME = "sha256"
    HASHMOD = hashlib.sha256


class RS128Key(RSKey):
    DIGESTSIZE = 320
    HASHNAME = "sha256"
    HASHMOD = hashlib.sha256


class RS256Key(RSKey):
    DIGESTSIZE = 512
    HASHNAME = "sha256"
    HASHMOD = hashlib.sha256


class DS128Key(DSKey):
    BITLENGTH = 160
    HASHMOD = hashlib.sha1


class DS256Key(DSKey):
    BITLENGTH = 256
    HASHMOD = hashlib.sha256
