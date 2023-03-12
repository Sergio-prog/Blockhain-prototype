import time
from hashlib import sha256
import json


class Block:

    def __init__(self, timestamp=None, data=None):
        self.timestamp = timestamp or time.time()
        self.data = [] if data is None else data
        self.prevHash = None  # хеш предыдущего блока
        self.nonce = 0
        self.hash = self.getHash()

    def getHash(self):
        hash = sha256()
        hash.update(str(self.prevHash).encode('utf-8'))
        hash.update(str(self.timestamp).encode('utf-8'))
        hash.update(str(self.data).encode('utf-8'))
        hash.update(str(self.nonce).encode('utf-8'))
        return hash.hexdigest()

    def mine(self, difficulty):  # Сложность вычисления нового хеща
        while self.hash[:difficulty] != '0' * difficulty:
            self.nonce += 1
            self.hash = self.getHash()


class Blockchain:

    def __init__(self):
        self.chain = [Block(str(int(time.time())))]
        self.difficulty = 1
        self.blockTime = 30000

    def __repr__(self):
        return json.dumps([{'data': item.data, 'timestamp': item.timestamp, 'nonce': item.nonce, 'hash': item.hash,
                            'prevHash': item.prevHash} for item in self.chain], indent=4)

    def getLastBlock(self):
        return self.chain[len(self.chain) - 1]

    def addBlock(self, block):
        block.prevHash = self.getLastBlock().hash
        block.hash = block.getHash()
        block.mine(self.difficulty)
        self.chain.append(block)

        self.difficulty += (-1, 1)[int(time.time()) - int(self.getLastBlock().timestamp) < self.blockTime]

    def isValid(self):
        for i in range(1, len(self.chain)):
            currentBlock = self.chain[i]
            prevBlock = self.chain[i - 1]

            if currentBlock.hash != currentBlock.getHash() or prevBlock.hash != prevBlock.prevHash:
                return False

            return True
