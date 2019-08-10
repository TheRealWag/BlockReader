#!/usr/bin/python3.7
from block_file import BlockFile

filename = "sample_block_bin"

print("Reading block from file: %s" % filename)
block = BlockFile(filename=filename).block
print("Read %d transactions from block\n" % len(block.transactions))

print("Getting the longest 100 transactions of the block")
top_txs = block.get_top_transactions(100)
print("Top 100 transactions indices:")
top_ids = [i.index for i in top_txs.values()]
print(top_ids)
print("\n")

# Longest transaction
hash1 = 'fff955fd2cbbe532b9c65db1932b186eda3e8e96abf1fd14ce96e631c5e00b61'

# Shortest transaction
hash2 = '1b14b80dba023c59856ad22a3c2075f4ea220b2739f3711f1b219a16255479e7'

print("Checking if %s is in top 100:" % hash1)
if block.is_tx_in_top_n(hash1, 100):
    print("Success")
else:
    print("Failed")

print("\n")

print("Checking if %s is not in top 100:" % hash2)
if block.is_tx_in_top_n(hash2, 100):
    print("Failed")
else:
    print("Success")

print("\n")

print("Details for Transaction %s:" % hash1)
print("Sequence position in block: %d" % block.transactions[hash1].index)
print("Hash value: %s" % block.transactions[hash1].hash)
print("Length: %d" % block.transactions[hash1].size)
print("Starting at offset: %d" % block.transactions[hash1].start_offset)
print("Ending at offset: %d" % block.transactions[hash1].end_offset)
