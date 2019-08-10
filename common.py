#!/usr/bin/python3.7
import struct


def get_vint(hex_data):
    """
    Returns the size and the value for the first variable length integer from raw hex data:
        (size, value)
    """
    int_size = int(hex_data[0])

    # if uint8, size is 1 and value is the int_size
    if int_size < 253:
        return 1, int_size

    # find if size of uint is 16, 32 or 64
    if int_size == 253:
        int_type = "<H"  # uint16
    elif int_size == 254:
        int_type = "<I"  # uint32
    else:
        int_type = "<Q"  # uint64

    # Get the size from the int_type
    n_bytes = struct.calcsize(int_type) + 1
    value = struct.unpack(int_type, hex_data[1:n_bytes])[0]

    return n_bytes, value
