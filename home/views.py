from django.shortcuts import render, HttpResponse
from django.http import JsonResponse
from .blockchain import Blockchain
import json as JSON
from uuid import uuid4
from urllib.parse import urlparse


node_address = str(uuid4()).replace('-', '')

blockchain = Blockchain()


def home(request):
    context = {}
    return render(request, 'home/index.html', context=context)


def mine_block(request):
    previous_block = blockchain.get_previous_block()
    previous_proof = previous_block['proof']
    proof = blockchain.proof_of_work(previous_proof)
    previous_hash = blockchain.hash(previous_block)
    # blockchain.add_transactions(sender = node_address, reciever = 'Prakhar',amount = 10)

    # Added by Kshitiz
    blockchain.sync_transactions()

    block = blockchain.create_block(proof, previous_hash)

    # Added by Kshitiz
    blockchain.empty_transactions()
    response = {
        'message': "Congratulations, You just mined a block!!",
        'index': block['index'],
        'timestamp': block['timestamp'],
        'proof': block['proof'],
        'previous_hash': block['previous_hash'],
        'transactions': block['transactions'],
    }
    return JsonResponse(response)


def get_chain(request):
    response = {
        'chain': blockchain.chain,
        'length': len(blockchain.chain),
    }
    return JsonResponse(response)


def is_valid(request):
    is_valid = blockchain.is_chain_valid(blockchain.chain)
    if is_valid:
        response = {
            'message': "All good !!! Nothing to worry about. Blockchain is valid."}
    else:
        response = {
            'message': "Nope... So, we got issues.. blockchain not valid !!!"}
    return JsonResponse(response)


def add_employment_transaction(request):
    if request.method == 'POST':
        record_data = request.POST
        # transaction_keys = ['recordType', 'recordData']
        # if not all(key in json for key in transaction_keys):
        # 	return "Some elements of transaction are misssing" , 400
        # record_data = json['recordData']
        index = blockchain.add_employment_transactions(
            record_data['employee_name'],
            record_data['employee_uid'],
            record_data['employer_name'],
            record_data['employer_uid'],
            record_data['start_date'],
            record_data['end_date']
        )
        response = {
            'message': f'The employment transaction will be added to block {index}'}
        return JsonResponse(response)


def add_criminal_transaction(request):
    if request.method == "POST":
        record_data = request.POST
        # transaction_keys = ['recordType','recordData']
        # if not all (key in json for key in transaction_keys):
        # 	return "Some elements of transaction are misssing" , 400
        # record_data = json['recordData']
        index = blockchain.add_criminal_transactions(
            record_data['accused_name'],
            record_data['accused_uid'],
            record_data['offence_details'],
            record_data['police_station_uid'],
            record_data['state_head'],
            record_data['status'],
            record_data['ipc_rule'],
        )
        response = {
            'message': f'The criminal transaction will be added to block {index}'}
        return JsonResponse(response)


def add_health_transaction(request):
    if request.method == "POST":
        record_data = request.POST
        # transaction_keys = ['recordType','recordData']
        # if not all (key in json for key in transaction_keys):
        # 	return "Some elements of transaction are misssing" , 400
        # record_data = json['recordData']
        index = blockchain.add_health_transactions(
            record_data['name'],
            record_data['uid'],
            record_data['fingerprint'],
            record_data['retina_scan'],
            record_data['vaccinations'],
            record_data['medicines'],
            record_data['major_accidents']
        )
        response = {
            'message': f'The health transaction will be added to block {index}'}
        return JsonResponse(response)


def connect_node(request):
    current_node = urlparse(request.build_absolute_uri())
    current_node = "http://" + str(current_node.netloc)
    content_string = None
    nodes = None
    with open('static/nodes.json', 'r') as file:
        content_string = file.read()
    content = JSON.loads(content_string)
    if content is not None:
        nodes = content['nodes']
    else:
        return HttpResponse("Something went wrong!")
    if nodes is None:
        return HttpResponse("No nodes in network!")
    for node in nodes:
        if current_node != str(node):
            blockchain.add_node(node)
    response = {
        "message": "All nodes are connected. The Blockchainly blockchain contains following nodes:",
        "total_nodes": list(blockchain.nodes)
    }
    return JsonResponse(response)


def replace_chain(request):
    is_chain_replaced = blockchain.replace_chain()
    if is_chain_replaced:
        response = {
            'message': "The nodes had different chains so chain was replaced by the longest one.",
            'new_chain': blockchain.chain
        }
    else:
        response = {
            'message': "All good. The chain was largest one.",
            'actual_chain': blockchain.chain
        }
    return JsonResponse(response)


def get_transactions(request):
    response = {
        'number_of_transactions': len(blockchain.transactions),
        'transactions': blockchain.transactions,
    }
    return JsonResponse(response)


def empty_transactions(request):
    blockchain.transactions = []
    response = {'message': 'Transactions were successfully emptied'}
    return JsonResponse(response)


def all_transactions(request):
    blockchain.sync_transactions()
    transactions = blockchain.transactions
    total_transactions = []
    if len(transactions) != 0:
        for transaction in transactions:
            print(transaction)
            total_transactions.append(
                {'status': 'pending', 'transaction': transaction})

    if len(blockchain.chain) != 0:
        for block in blockchain.chain:
            for transaction in block["transactions"]:
                total_transactions.append(
                    {'status': 'completed', 'transaction': transaction, 'timestamp': block["timestamp"]})

    response = {
        'number_of_pending_transactions': len(blockchain.transactions),
        'number_of_completed_transactions': len(total_transactions)-len(blockchain.transactions),
        'total_transactions': total_transactions,
    }
    return JsonResponse(response)


def fetch_record(request, record_type, public_key):
    # chain = blockchain.chain
    # required_transaction = []
    # for block in chain:
    #     transactions = block['transactions']
    #     if transactions:
    #         for transaction in transactions:
    #             record_type = transaction['recordType']
    #             if str(record_type) == str(record_type):
    #                 record_data = transaction['recordData']
    #                 name =
    return HttpResponse("fgg")