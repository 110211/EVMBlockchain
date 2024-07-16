from flask import Flask, jsonify, request
from blockchain import blockchain, proof_of_work, proof_of_stake, broadcast_new_block, register_node, consensus, verify_signature, get_balance, shards, nodes, validators, previous_block
from governance import proposals, create_proposal, vote_proposal, get_proposals
from monitoring import monitoring_info, update_monitoring_info
import time  # Thêm thư viện time

app = Flask(__name__)

@app.route('/register_node', methods=['POST'])
def register_node_endpoint():
    data = request.get_json()
    node_url = data.get('node_url')
    if node_url:
        register_node(node_url)
        return jsonify({'message': 'Node registered successfully', 'nodes': list(nodes)}), 201
    else:
        return jsonify({'message': 'Invalid node URL'}), 400

@app.route('/consensus', methods=['GET'])
def consensus_endpoint():
    replaced = consensus()
    if replaced:
        return jsonify({'message': 'Our chain was replaced', 'new_chain': [block.__dict__ for block in blockchain]}), 200
    else:
        return jsonify({'message': 'Our chain is authoritative', 'chain': [block.__dict__ for block in blockchain]}), 200

@app.route('/send_transaction', methods=['POST'])
def send_transaction():
    data = request.get_json()
    transaction = data['transaction']
    signature = data['signature']
    public_key = data['public_key']

    if verify_signature(transaction, signature, public_key):
        sender_balance = get_balance(transaction['sender'])
        if sender_balance >= transaction['amount']:
            # Phân chia giao dịch vào các shard
            if transaction['amount'] % 2 == 0:
                shards['shard_1'].append(transaction)
            else:
                shards['shard_2'].append(transaction)
            response = {'message': f'Transaction will be added to shard', 'shards': shards}
            return jsonify(response), 201
        else:
            return 'Insufficient balance', 400
    else:
        return 'Transaction verification failed', 400

@app.route('/new_block', methods=['POST'])
def new_block():
    global blockchain, previous_block, transactions

    start_time = time.time()
    new_block = proof_of_work(previous_block, transactions)
    end_time = time.time()

    blockchain.append(new_block)
    previous_block = new_block
    transactions = []
    shards['shard_1'] = []
    shards['shard_2'] = []

    # Cập nhật thông tin giám sát
    update_monitoring_info('proof_of_work', start_time, end_time)

    response = {
        'message': 'New block created',
        'block': {
            'index': new_block.index,
            'timestamp': new_block.timestamp,
            'transactions': new_block.transactions,
            'previous_hash': new_block.previous_hash,
            'current_hash': new_block.current_hash,
            'nonce': new_block.nonce
        }
    }

    broadcast_new_block(new_block)
    return jsonify(response), 201

@app.route('/new_block_pos', methods=['POST'])
def new_block_pos():
    global blockchain, previous_block, transactions

    if not validators:
        return 'No validators registered', 400

    start_time = time.time()
    transactions = shards['shard_1'] + shards['shard_2']
    new_block = proof_of_stake(previous_block, transactions)
    end_time = time.time()

    blockchain.append(new_block)
    previous_block = new_block
    transactions = []
    shards['shard_1'] = []
    shards['shard_2'] = []

    # Cập nhật thông tin giám sát
    update_monitoring_info('proof_of_stake', start_time, end_time)

    response = {
        'message': 'New block created using PoS',
        'block': {
            'index': new_block.index,
            'timestamp': new_block.timestamp,
            'transactions': new_block.transactions,
            'previous_hash': new_block.previous_hash,
            'current_hash': new_block.current_hash,
            'validator': new_block.validator
        }
    }

    broadcast_new_block(new_block)
    return jsonify(response), 201

@app.route('/get_chain', methods=['GET'])
def get_chain():
    chain_data = []
    for block in blockchain:
        chain_data.append({
            'index': block.index,
            'timestamp': block.timestamp,
            'transactions': block.transactions,
            'previous_hash': block.previous_hash,
            'current_hash': block.current_hash,
            'nonce': block.nonce
        })
    return jsonify({'length': len(chain_data), 'chain': chain_data})

@app.route('/create_proposal', methods=['POST'])
def create_proposal_endpoint():
    return create_proposal()

@app.route('/vote_proposal', methods=['POST'])
def vote_proposal_endpoint():
    return vote_proposal()

@app.route('/get_proposals', methods=['GET'])
def get_proposals_endpoint():
    return get_proposals()

@app.route('/monitoring_info', methods=['GET'])
def get_monitoring_info():
    return jsonify(monitoring_info), 200

if __name__ == '__main__':
    app.run(port=5000)
