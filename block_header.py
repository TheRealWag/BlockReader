#!/usr/bin/python3.7
class BlockHeader:
    """Represents the header of a block"""
    def __init__(self, raw_data):
        self.version = raw_data[:4]
        self.previous_hash = raw_data[4:36]
        self.merkle_root = raw_data[36:68]
        self.timestamp = raw_data[68:72]
        self.bits = raw_data[72:76]
        self.nonce = raw_data[76:80]
