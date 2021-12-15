import hashlib
import json
import logging
import sys
import time
import utils

logging.basicConfig(level=logging.INFO, stream=sys.stdout)
logger = logging.getLogger(__name__)
MININING_DIDDICULTY = 3
MINING_SENDER = "The blockchain"
MINING_REWARD = 1.0


class Blockchain(object):
    def __init__(self, blockchain_address=None):
        self.transaction_pool = []
        self.chain = []
        self.create_block(0, self.hash({}))
        self.blockchain_address = blockchain_address

    def create_block(self, nonce, previous_hash):
        block = utils.sorted_dict_by_key({
            "timestamp": time.time(),
            "transactions": self.transaction_pool,
            "nonce": nonce,
            "previous_hash": previous_hash,
        })

        self.chain.append(block)
        self.transaction_pool = []
        return block

    # ハッシュ化を行う
    def hash(self, block):
        # ダブルチェックする
        # jsonをソートしながらstringにする
        sorted_block = json.dumps(block, sort_keys=True)
        return hashlib.sha256(sorted_block.encode()).hexdigest()

    def add_transaction(self, sender_blockchain_address, recipient_blockchain_address, value):
        transaction = utils.sorted_dict_by_key({
            "sender_blockchain_address": sender_blockchain_address,
            "recipient_blockchain_address": recipient_blockchain_address,
            "value": float(value)
        })

        self.transaction_pool.append(transaction)

        return True

    def valid_proof(self, transactions, previous_hash, nonce, difficulty=MININING_DIDDICULTY):
        guess_block = utils.sorted_dict_by_key({
            "transactions": transactions,
            "nonce": nonce,
            "previous_hash": previous_hash
        })

        guess_hash = self.hash(guess_block)
        # 初めの先頭が000であればTrueを返す。
        return guess_hash[:difficulty] == "0" * difficulty

    def proof_of_work(self):
        transactions = self.transaction_pool.copy()
        # 最後にチェインしたものをとってこれる
        previous_hash = self.hash(self.chain[-1])

        nonce = 0
        while self.valid_proof(transactions, previous_hash, nonce) is False:
            nonce += 1
        return nonce

    def mining(self):
        # トランザクションの追加
        self.add_transaction(
            sender_blockchain_address=MINING_SENDER,
            recipient_blockchain_address=self.blockchain_address,
            value=MINING_REWARD)

        nonce = self.proof_of_work()
        # 前のハッシュ値を受け取り
        previous_hash = self.hash(self.chain[-1])

        # ブロックの生成
        self.create_block(nonce, previous_hash)
        logger.info({"action": "mining", "status": "success"})
        return True

    # トータルを計算する
    def calclate_total_amount(self, blockchain_address):
        total_amount = 0.0
        for block in self.chain:
            for transaction in block["transactions"]:
                value = float(transaction["value"])

                if blockchain_address == transaction["recipient_blockchain_address"]:
                    total_amount += value
                if blockchain_address == transaction["sender_blockchain_address"]:
                    total_amount -= value
        return total_amount


if __name__ == '__main__':
    my_blockchain_address = "test_mamushi"
    block_chain = Blockchain(blockchain_address=my_blockchain_address)
    utils.pprint(block_chain.chain)

    block_chain.add_transaction("A", "B", 1.0)

    # 一番最後の要素をハッシュ化する
    block_chain.mining()
    utils.pprint(block_chain.chain)

    block_chain.add_transaction("C", "D", 2.0)
    block_chain.add_transaction("X", "Y", 3.0)

    block_chain.mining()
    utils.pprint(block_chain.chain)

    print("my", block_chain.calclate_total_amount(my_blockchain_address))
