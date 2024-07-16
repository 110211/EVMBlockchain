import hashlib
import time
import requests
from uuid import uuid4
import ecdsa  # Thêm thư viện ecdsa
import random  # Thêm thư viện random để chọn validator trong PoS

class Block:
    def __init__(self, index, previous_hash, timestamp, transactions, current_hash, nonce=0, validator=None):
        self.index = index
        self.previous_hash = previous_hash
        self.timestamp = timestamp
        self.transactions = transactions
        self.current_hash = current_hash
        self.nonce = nonce
        self.validator = validator

def calculate_hash(index, previous_hash, timestamp, transactions, nonce=0):
    value = str(index) + str(previous_hash) + str(timestamp) + str(transactions) + str(nonce)
    return hashlib.sha256(value.encode('utf-8')).hexdigest()

def create_genesis_block():
    return Block(0, "0", int(time.time()), "Genesis Block", calculate_hash(0, "0", int(time.time()), "Genesis Block"))

class Transaction:
    def __init__(self, sender, recipient, amount, signature):
        self.sender = sender
        self.recipient = recipient
        self.amount = amount
        self.signature = signature

    def to_dict(self):
        return {
            'sender': self.sender,
            'recipient': self.recipient,
            'amount': self.amount,
            'signature': self.signature
        }

blockchain = [create_genesis_block()]
previous_block = blockchain[0]
transactions = []
validators = []
nodes = set()
shards = {'shard_1': [], 'shard_2': []}  # Tạo 2 shard để phân chia giao dịch

def proof_of_work(previous_block, transactions):
    index = previous_block.index + 1
    timestamp = int(time.time())
    previous_hash = previous_block.current_hash
    nonce = 0
    while True:
        hash_value = calculate_hash(index, previous_hash, timestamp, transactions, nonce)
        if hash_value.startswith('0000'):
            return Block(index, previous_hash, timestamp, transactions, hash_value, nonce)
        nonce += 1

def proof_of_stake(previous_block, transactions):
    index = previous_block.index + 1
    timestamp = int(time.time())
    previous_hash = previous_block.current_hash
    validator = select_validator(validators)
    nonce = 0

    hash_value = calculate_hash(index, previous_hash, timestamp, transactions, nonce)
    return Block(index, previous_hash, timestamp, transactions, hash_value, validator=validator)

def select_validator(validators):
    return random.choice(validators)

def sign_transaction(transaction, private_key):
    private_key_bytes = bytes.fromhex(private_key)
    sk = ecdsa.SigningKey.from_string(private_key_bytes, curve=ecdsa.SECP256k1)
    message = f"{transaction['sender']}:{transaction['recipient']}:{transaction['amount']}"
    signature = sk.sign(message.encode())
    return signature.hex()

def verify_signature(transaction, signature, public_key):
    public_key_bytes = bytes.fromhex(public_key)
    vk = ecdsa.VerifyingKey.from_string(public_key_bytes, curve=ecdsa.SECP256k1)
    message = f"{transaction['sender']}:{transaction['recipient']}:{transaction['amount']}"
    try:
        return vk.verify(bytes.fromhex(signature), message.encode())
    except ecdsa.BadSignatureError:
        return False

def get_balance(address):
    balance = 0
    for block in blockchain:
        for tx in block.transactions:
            if tx['sender'] == address:
                balance -= tx['amount']
            if tx['recipient'] == address:
                balance += tx['amount']
    return balance

def register_node(node_url):
    nodes.add(node_url)

def consensus():
    global blockchain
    longest_chain = None
    max_length = len(blockchain)

    for node in nodes:
        response = requests.get(f'{node}/get_chain')
        if response.status_code == 200:
            length = response.json()['length']
            chain = response.json()['chain']

            if length > max_length:
                max_length = length
                longest_chain = chain

    if longest_chain:
        blockchain = [Block(**block) for block in longest_chain]
        return True

    return False

def broadcast_new_block(new_block):
    for node in nodes:
        requests.post(f'{node}/new_block', json=new_block.__dict__)
