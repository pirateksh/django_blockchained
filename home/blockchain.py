import datetime
import hashlib
import json
import requests
from urllib.parse import urlparse


class Blockchain:
    
    def __init__(self):
        self.chain = []
        self.transactions = []
        self.create_block(proof=1, previous_hash='0')
        self.nodes = set()
        self.transaction_types = set()
         
    def create_block(self, proof, previous_hash):
        block = {
            "index": len(self.chain)+1,
            "timestamp": str(datetime.datetime.now()),
            "proof": proof,
            "previous_hash": previous_hash,
            "transactions": self.transactions,
        }
        self.transactions = []
        self.chain.append(block)
        return block 

    def get_previous_block(self):
        return self.chain[-1]
    
    def proof_of_work(self, previous_proof):
        new_proof = 1 
        check_proof = False
        while check_proof is False:
            hash_operation = hashlib.sha256(str(new_proof**2 - previous_proof**2).encode()).hexdigest()  
            if hash_operation[:4] == '0000':
                check_proof = True
            else:
                new_proof +=1 
        return new_proof 
    
    def hash(self, block):
        encoded_block = json.dumps(block, sort_keys = True).encode()
        return  hashlib.sha256(encoded_block).hexdigest()
    
    def is_chain_valid(self, chain):
        previous_block = chain[0]
        block_index = 1 
        while block_index < len(chain):
            block = chain[block_index]
            if block['previous_hash'] != self.hash(previous_block):
                return False
            previous_proof = previous_block['proof']
            proof = block['proof']
            hash_operation = hashlib.sha256(str(proof**2 - previous_proof**2).encode()).hexdigest()
            if hash_operation[:4] != '0000':
                return False
            previous_block = block
            block_index += 1
        return True  
    
    def add_employment_transactions(self, employeeName, employeeUID, employerName, employerUID, startDate, endDate):
        self.transactions.append({
            "recordType": "employment",
            "recordData": {
                "employeeName": employeeName,
                "employeeUID": employeeUID,
                "employerName": employerName,
                "employerUID": employerUID,
                "startDate": startDate,
                "endDate": endDate,
            },
        })
        previous_block = self.get_previous_block()
        return previous_block['index'] + 1

    def add_criminal_transactions(self, accusedUID, accusedName, offenceDetails, policeStationUID, stateHead, status, IPCRule):
        self.transactions.append({
            "recordType": "criminal",
            "recordData": {
                "accusedUID": accusedUID,
                "accusedName": accusedName,
                "offenceDetails": offenceDetails,
                "policeStationUID": policeStationUID,
                "stateHead": stateHead,
                "status": status,
                "IPCRule": IPCRule
            }
        })
        previous_block = self.get_previous_block()
        return previous_block['index'] + 1

    def add_health_transactions(self, name, UID, fingerprint, retinaScan, vaccinations, medicines, majorAccidents):
        self.transactions.append({
            "recordType": "health",
            "recordData": {
                "name": name,
                "UID": UID,
                "fingerprint": fingerprint,
                "retinaScan": retinaScan,
                "vaccinations": vaccinations,
                "medicines": medicines,
                "majorAccidents": majorAccidents
            }
        })
        previous_block = self.get_previous_block()
        return previous_block['index'] + 1

    def add_node(self, address):
        parsed_url = urlparse(address)
        self.nodes.add(parsed_url.netloc)

    def add_transaction_type(self, transaction_type):
        self.transaction_types.add(transaction_type)

    def replace_chain(self):
        network = self.nodes
        longest_chain = None
        max_length = len(self.chain)
        for node in network:
            url = f'http://{node}/get_chain'
            response = requests.get(url)
            if response.status_code == 200:
                length = response.json()['length']
                chain = response.json()['chain']
                if length > max_length and self.is_chain_valid(chain):
                    max_length = length
                    longest_chain = chain
        
        if longest_chain: 
            self.chain = longest_chain
            return True
        return False

    def sync_transactions(self):
        network = self.nodes
        record_type = None
        record_data = None
        transactions_in_node = None
        for node in network:
            response = requests.get(f'http://{node}/get_transactions/')
            if response.status_code == 200:
                transactions_in_node = response.json()['transactions']
                if transactions_in_node:
                    for transaction in transactions_in_node:
                        record_type = transaction['recordType']
                        record_data = transaction['recordData']
                        if record_type and record_data:
                            if record_type == "criminal":
                                self.add_criminal_transactions(
                                    record_data['accusedName'],
                                    record_data['accusedUID'],
                                    record_data['offenceDetails'],
                                    record_data['policeStationUID'],
                                    record_data['status'],
                                    record_data['IPCRule'],
                                    record_data['stateHead']
                                )
                            if record_type == "employment":
                                self.add_employment_transactions(
                                    record_data['employeeName'],
                                    record_data['employeeUID'],
                                    record_data['employerName'],
                                    record_data['employerUID'],
                                    record_data['startDate'],
                                    record_data['endDate']
                                )
                            if record_type == "health":
                                self.add_health_transactions(
                                    record_data['name'],
                                    record_data['UID'],
                                    record_data['fingerprint'],
                                    record_data['retinaScan'],
                                    record_data['vaccinations'],
                                    record_data['medicines'],
                                    record_data['majorAccidents']
                                )
        if transactions_in_node:
            return True
        return False

    def empty_transactions(self):
        network = self.nodes
        for node in network:
            response = requests.get(f'http://{node}/empty_transactions/')
            if response.status_code != 200:
                return False
        return True











