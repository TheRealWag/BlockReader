#!/usr/bin/python3.7
import hashlib
from common import get_vint

from block_header import BlockHeader
from transaction import Transaction


class Block:
    """Represents a block of transactions"""
    def __init__(self, raw_data):
        self.header = BlockHeader(raw_data[:80])
        self.hash = hashlib.sha256(hashlib.sha256(raw_data[:80]).digest()).digest().hex()
        self.transactions = {}
        self.transactions = {tx.hash: tx for tx in self._get_transactions(raw_data[80:])}

    @staticmethod
    def _get_transactions(raw_data):
        """Returns iterator for a block's transactions"""
        # Get the number of transactions
        offset, n_txs = get_vint(raw_data[:9])

        for i in range(n_txs):
            # Start with chunk size of 512 bytes and multiply it by 2 each time we get index error (up to 32 mb)
            chunk = 512
            for j in range(16):
                try:
                    tx = Transaction(raw_data[offset:offset + chunk])
                    break
                except IndexError:
                    chunk *= 2
            tx.index = i
            tx.start_offset = offset
            tx.end_offset = tx.start_offset + tx.size
            offset += tx.size
            yield tx

    def get_top_transactions(self, n=100):
        """Returns the top n (default is 100) transactions of the block"""
        if len(self.transactions) < n:
            return dict(sorted(self.transactions.items(), key=lambda x: x[1], reverse=True))
        else:
            return dict(sorted(self.transactions.items(), key=lambda x: x[1], reverse=True)[:n])

    def is_tx_in_top_n(self, h, n):
        """Returns true if a transaction with the hash h is in the top n transactions of the block"""
        return h in self.get_top_transactions(n)

