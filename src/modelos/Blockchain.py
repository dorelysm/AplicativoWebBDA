from hashlib import sha256
import json
from time import time
from uuid import uuid4
from flask import Flask, jsonify, request
from flask_cors import CORS

class Blockchain:
    def __init__(self) -> None:
        self.chain = []
        self.pending_transactions = []

        self.new_block(previous_hash = 'genesis', proof = 100)

    def new_block(self, proof, previous_hash = None):
        block = {
            'index': len(self.chain),
            'timestamp': time(),
            'transactions': self.pending_transactions,
            'proof': proof,
            'previous_hash': previous_hash or self.hash(self.chain[-1]),
        }
        self.pending_transactions = []
        self.chain.append(block)
        return block
    
    def new_transaction(self, sender, recipient, amount):
        self.pending_transactions.append({
            'sender': sender,
            'recipient': recipient,
            'amount': amount
        })

    @staticmethod
    def hash(block):
        block_string = json.dumps(block, sort_keys=True).encode()
        return sha256(block_string).hexdigest()
    
    @property
    def last_block(self):
        return self.chain[-1]
    
    def proof_of_work(self):
        last_proof = self.last_block['proof']
        proof = 0
        
        while self.valid_proof(last_proof, proof) is False:
            proof +=1
            return proof
        
    @staticmethod
    def valid_proof(last_proof, proof):
        guess = f'{last_proof}{proof}'.encode()
        guess_hash = sha256(guess).hexdigest()
        return guess_hash[:4] == '0000'
    
