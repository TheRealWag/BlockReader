#!/usr/bin/python3.7
from block import Block


class BlockFile:
    """Represents a block message from a block file"""

    def __init__(self, filename="sample_block_bin"):
        file = open(filename, "rb")

        b_magic = file.read(4)
        b_command = file.read(12)
        b_length = file.read(4)
        b_cksum = file.read(4)

        self._block = None

        self.magic = int.from_bytes(b_magic, byteorder='little')
        self.command = b_command.decode()
        self.length = int.from_bytes(b_length, byteorder='little')
        self.cksum = int.from_bytes(b_cksum, byteorder='little')

        self.payload = file.read(self.length)

        file.close()

    @property
    def block(self):
        if self._block is None:
            self._block = Block(self.payload)
        return self._block
