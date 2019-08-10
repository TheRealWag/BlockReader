#!/usr/bin/python3.7
import hashlib
import struct

from common import get_vint


class Input:
    """Represents a transaction's input"""
    def __init__(self, raw_data):
        # Skip the first 36 bytes (previous output)
        cursor = 36

        # Get script length
        vint_size, script_length = get_vint(raw_data[cursor:cursor+9])
        cursor += vint_size

        # Size of input is offset + script_length + sequence
        self.size = cursor + script_length + 4

        # Store the input data
        self.data = raw_data[:self.size]

        # Witness list is populated when the transaction is parsed
        self.witnesses = []


class Output:
    """Represents a transaction's output"""
    def __init__(self, raw_data):
        # Read the output value from the first 8 bytes
        self.value = struct.unpack("<Q", raw_data[:8])[0]
        cursor = 8

        # Get the output script
        vint_size, script_length = get_vint(raw_data[8:17])
        cursor += vint_size
        self.script = raw_data[cursor:cursor + script_length]
        cursor += script_length

        self.size = cursor
        self.data = raw_data[:self.size]


class Transaction:
    """Represents a transaction"""
    def __init__(self, raw_data):
        self.index = None
        self.start_offset = None
        self.end_offset = None
        self._is_witnesses = False

        # Get version from first 4 bytes
        self.version = raw_data[:4]
        cursor = 4

        # Check if this tx supports segwit
        if raw_data[cursor:cursor + 2] == b'\x00\x01':
            self._is_witnesses = True
            cursor += 2

        # Get the number of inputs
        vint_size, n_inputs = get_vint(raw_data[cursor:cursor+9])
        cursor += vint_size

        # Get inputs
        self.inputs = []
        for i in range(n_inputs):
            tx_input = Input(raw_data[cursor:])
            self.inputs.append(tx_input)
            cursor += tx_input.size

        # Get the number of outputs
        vint_size, n_outputs = get_vint(raw_data[cursor:cursor+9])
        cursor += vint_size

        # Get outputs
        self.outputs = []
        for i in range(n_outputs):
            tx_output = Output(raw_data[cursor:])
            self.outputs.append(tx_output)
            cursor += tx_output.size

        # Get witnesses if segwit is enabled
        if self._is_witnesses:
            for i in self.inputs:
                vint_size, n_wits = get_vint(raw_data[cursor:cursor+9])
                cursor += vint_size
                for w in range(n_wits):
                    vint_size, wit_len = get_vint(raw_data[cursor:cursor+9])
                    cursor += vint_size
                    wit = raw_data[cursor:cursor + wit_len]
                    i.witnesses.append(wit)
                    cursor += wit_len

        # Skip last 4 bytes (lock_time)
        cursor += 4

        self.size = cursor
        self.data = raw_data[:self.size]
        self.hash = hashlib.sha256(hashlib.sha256(self.data).digest()).digest().hex()

    # Some compare functions to make the object sortable
    def __lt__(self, other):
        assert(isinstance(other, Transaction))
        return self.size < other.size

    def __le__(self, other):
        assert (isinstance(other, Transaction))
        return self.size <= other.size

    def __eq__(self, other):
        assert (isinstance(other, Transaction))
        return self.size == other.size

    def __ne__(self, other):
        assert (isinstance(other, Transaction))
        return self.size != other.size

    def __gt__(self, other):
        assert (isinstance(other, Transaction))
        return self.size > other.size

    def __ge__(self, other):
        assert (isinstance(other, Transaction))
        return self.size >= other.size
