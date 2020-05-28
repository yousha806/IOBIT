
from hashli import sha256
import time
import random
import string
import json
import binascii
import logging
import datetime
import collections
import Crypto
import Crypto.Random
from Crypto.Hash import SHA
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5

class Client:
    def __init__(self):
      random = Crypto.Random.new().read
      self._private_key = RSA.generate(1024)
      self._public_key = self._private_key.publickey()
      self._signer = PKCS1_v1_5.new(self._private_key)
    @property
    def identity(self):
        return binascii.hexlify(self._public_key.exportKey(format='DER')).decode('ascii')
Manipal=Client()

class Transaction:
    def __init__(self, sender, recipient, value):
     self.sender = sender
     self.recipient = recipient
     self.value = value
     self.time = datetime.datetime.now()
    def to_dict(self):
         if self.sender == "Genesis":
            identity = "Genesis"
         else:
            identity = self.sender.identity
         return collections.OrderedDict({'sender': identity,
                        'recipient': self.recipient,
                        'value': self.value,
                        'time' : self.time})
    def sign_transaction(self):
         private_key = self.sender._private_key
         signer = PKCS1_v1_5.new(private_key)
         h = SHA.new(str(self.to_dict()).encode('utf8'))
         return binascii.hexlify(signer.sign(h)).decode('ascii')   
Amazon=Client()
t1=Transaction(Amazon,Manipal.identity,3)
signature=t1.sign_transaction()#generates signature for t1
print(signature)
def display_transaction(transaction):
    #for transaction in transactions:
         dict = transaction.to_dict()
         print ("sender: " + dict['sender'])
         print ('-----')
         print ("recipient: " + dict['recipient'])
         print ('-----')
         print ("value: " + str(dict['value']))
         print ('-----')
         print ("time: " + str(dict['time']))
         print ('-----')
t1.sign_transaction()
pending_transaction=[]
pending_transaction.append(t1)
for transaction in pending_transaction:
    display_transaction (transaction)
    print('----------')
class Block: 
    def __init__(self, index, transactions, timestamp, previous_hash): 
        self.index = index 
        self.transactions = transactions 
        self.timestamp = timestamp
        self.previous_hash = previous_hash 
 
    def compute_hash(self): 
        block_string = json.dumps(self.__dict__, sort_keys=True) 
        return sha256(block_string.encode()).hexdigest()
class Blockchain:
 
    def __init__(self):
        self.pending_transaction=[]
        self.chain = []
        self.create_genesis_block()
 
    def create_genesis_block(self):
        
        genesis_block = Block(0, [], time.time(), "0")
        genesis_block.hash = genesis_block.compute_hash()
        self.chain.append(genesis_block)
 
    @property
    def last_block(self):
        return self.chain[-1]
    difficulty=3
    def proof_of_work(self, block):
       
        block.nonce = 0
 
        computed_hash = block.compute_hash()
        while not computed_hash.startswith('0' * Blockchain.difficulty):
            block.nonce += 1
            computed_hash = block.compute_hash()
 
        return computed_hash
        '''in order to check if the transaction is valid, one must check the 
        wallet of the sender to see if they are over spending. The signature should
        also be verified. Once the transaction is verified, it will be added from
        pending transaction to the block. The transaction, if unspent, will be present
        in the pending transaction dictionary. If it isnot present there, then
        transaction is spent, and invalid. Whoever solves the POW first as a miner,
        would be able to add the pending transaction to the block first'''
