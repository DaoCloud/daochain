from math import ceil

import eth_abi.abi
import web3.utils.abi
from eth_abi.abi import (
    process_type,
)
from eth_abi.exceptions import (
    EncodingError,
    ValueOutOfBounds,
)
from eth_abi.utils import ceil32, encode_int, is_numeric, is_string, is_text, to_string, zpad
from rlp.utils import (
    decode_hex,
)
from web3.utils.address import (
    is_address,
)
from web3.utils.types import is_array, is_boolean, is_integer, is_string

_is_encodable = web3.utils.abi.is_encodable


def is_encodable(_type, value):
    try:
        base, sub, arrlist = _type
    except ValueError:
        base, sub, arrlist = process_type(_type)

    if arrlist:
        if not is_array(value):
            return False
        if arrlist[-1] and len(value) != arrlist[-1][0]:
            return False
        sub_type = (base, sub, arrlist[:-1])
        return all(is_encodable(sub_type, sub_value) for sub_value in value)
    elif base == 'bool':
        return is_boolean(value)
    elif base == 'uint':
        if not is_integer(value):
            return False
        exp = int(sub)
        if value < 0 or value >= 2 ** exp:
            return False
        return True
    elif base == 'int':
        if not is_integer(value):
            return False
        exp = int(sub)
        if value <= -1 * 2 ** (exp - 1) or value >= 2 ** (exp - 1):
            return False
        return True
    elif base == 'string':
        if not is_string(value):
            return False
        return True
    elif base == 'bytes':
        if not is_string(value):
            return False

        if not sub:
            return True

        length = len(value)
        max_length = int(sub)
        if value.startswith('0x'):
            length = ceil(length / 2.0 - 1)
        return length <= max_length

    elif base == 'address':
        if not is_address(value):
            return False
        return True
    else:
        raise ValueError("Unsupported type")


_encode_single = eth_abi.abi.encode_single


def encode_single(typ, arg):
    try:
        base, sub, arrlist = typ
    except ValueError:
        base, sub, arrlist = process_type(typ)

    if is_text(arg):
        arg = to_string(arg)

    # Unsigned integers: uint<sz>
    if base == 'uint':
        sub = int(sub)
        i = decint(arg, False)

        if not 0 <= i < 2 ** sub:
            raise ValueOutOfBounds(repr(arg))
        return zpad(encode_int(i), 32)
    # bool: int<sz>
    elif base == 'bool':
        if not isinstance(arg, bool):
            raise EncodingError("Value must be a boolean")
        return zpad(encode_int(int(arg)), 32)
    # Signed integers: int<sz>
    elif base == 'int':
        sub = int(sub)
        i = decint(arg, True)
        if not -2 ** (sub - 1) <= i < 2 ** (sub - 1):
            raise ValueOutOfBounds(repr(arg))
        return zpad(encode_int(i % 2 ** sub), 32)
    # Unsigned reals: ureal<high>x<low>
    elif base == 'ureal':
        high, low = [int(x) for x in sub.split('x')]
        if not 0 <= arg < 2 ** high:
            raise ValueOutOfBounds(repr(arg))
        return zpad(encode_int(int(arg * 2 ** low)), 32)
    # Signed reals: real<high>x<low>
    elif base == 'real':
        high, low = [int(x) for x in sub.split('x')]
        if not -2 ** (high - 1) <= arg < 2 ** (high - 1):
            raise ValueOutOfBounds(repr(arg))
        i = int(arg * 2 ** low)
        return zpad(encode_int(i % 2 ** (high + low)), 32)
    # Strings
    elif base == 'string' or base == 'bytes':
        if not is_string(arg):
            raise EncodingError("Expecting string: %r" % arg)
        # Fixed length: string<sz>
        if len(sub):
            if int(sub) > 32:
                raise EncodingError("Fixed length strings must be 32 bytes or less")
            if len(arg) > int(sub):
                raise EncodingError(
                    "Value cannot exceed {0} bytes in length".format(sub)
                )
            return arg + b'\x00' * (32 - len(arg))
        # Variable length: string
        else:
            return zpad(encode_int(len(arg)), 32) + \
                   arg + \
                   b'\x00' * (ceil32(len(arg)) - len(arg))
    # Hashes: hash<sz>
    elif base == 'hash':
        if not (int(sub) and int(sub) <= 32):
            raise EncodingError("too long: %r" % arg)
        if is_numeric(arg):
            return zpad(encode_int(arg), 32)
        elif len(arg) == int(sub):
            return zpad(arg, 32)
        elif len(arg) == int(sub) * 2:
            return zpad(decode_hex(arg), 32)
        else:
            raise EncodingError("Could not parse hash: %r" % arg)
    # Addresses: address (== hash160)
    elif base == 'address':
        if sub != '':
            raise EncodingError("Address type cannot specify a byte size")
        if is_numeric(arg):
            return zpad(encode_int(arg), 32)
        elif len(arg) == 20:
            return zpad(arg, 32)
        elif len(arg) == 40:
            return zpad(decode_hex(arg), 32)
        elif len(arg) == 42 and arg[:2] == b'0x':
            return zpad(decode_hex(arg[2:]), 32)
        else:
            raise EncodingError("Could not parse address: %r" % arg)
    raise EncodingError("Unhandled type: %r %r" % (base, sub))


def patch_is_encodable():
    web3.utils.abi.is_encodable = is_encodable


def patch_encode_single():
    eth_abi.abi.encode_single = encode_single


def patch_all():
    patch_is_encodable()
    # patch_encode_single()
