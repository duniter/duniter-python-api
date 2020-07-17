# imports locally stored blockchain in the chunk format
# example usage :
# ```
# from duniterpy.localblockchain import load
# bc = load() # gets blockchain iterator
# b = next(bc) # gets block
# ```


import json
import os
import glob
from .documents import Block

CHUNK_SIZE = 250


class JsonBlockchain:
    def __init__(self, folder):
        self.folder = folder  # folder where chunks are stored
        self.chunks = len(
            glob.glob(os.path.join(folder, "chunk_*"))
        )  # number of files starting with "chunk_"
        self.current_block_in_chunk = (
            0  # number from 0 to 249 equal to current_block // current_chunk
        )
        self.current_chunk = 0  # current chunk number
        self.chunk = []  # parsed json for current chunk (length = 250)
        self.parsechunk()  # parse first chunk

    def parsechunk(self):
        """parse a json chunk file"""
        with open(
            os.path.join(self.folder, "chunk_" + str(self.current_chunk) + "-250.json")
        ) as f:
            s = f.read()
            p = json.loads(s)
            self.chunk = p["blocks"]

    def __iter__(self):
        return self

    def __next__(self):
        """if current block is outside current chunk, parse next one, otherwise, return current block parsed json"""
        if self.current_block_in_chunk == 250:  # block outside chunk
            self.current_block_in_chunk = 0  # reset to next chunk start
            self.current_chunk += 1  # increment current chunk number
            if self.current_chunk >= self.chunks:  # outside range
                raise StopIteration()
            self.parsechunk()  # parse this chunk
        self.current_block_in_chunk += (
            1  # increment current block number for next iteration
        )
        return self.chunk[
            self.current_block_in_chunk - 1
        ]  # return block (before incrementation)


def Blockchain(json_blockchain):
    """convert json to duniterpy block document"""
    jbc = json_blockchain
    for jb in jbc:
        yield Block.from_parsed_json(jb)


def load(path=".config/duniter/duniter_default/g1/"):
    """returns an iterator allowing to browse all the blockchain
    in practice, it will load chunk by chunk and only keep one in memory at a time"""
    path = os.path.join(os.path.expanduser("~"), path)  # expand path
    jbc = JsonBlockchain(path)  # gets an iterator over json blockchain
    bc = Blockchain(jbc)  # convert it to an iterator over blocks
    return bc  # returns
