from flask import jsonify, request
from collections import defaultdict

# Biến toàn cục để quản lý đề xuất và bỏ phiếu
proposals = []
votes = defaultdict(int)
proposal_threshold = 2  # Số phiếu cần thiết để thông qua đề xuất

class Proposal:
    def __init__(self, proposal_id, description, status='Pending'):
        self.proposal_id = proposal_id
        self.description = description
        self.status = status

    def to_dict(self):
        return {
            'proposal_id': self.proposal_id,
            'description': self.description,
            'status': self.status
        }

def create_proposal():
    data = request.get_json()
    proposal_id = len(proposals) + 1
    description = data.get('description')
    if description:
        proposal = Proposal(proposal_id, description)
        proposals.append(proposal)
        return jsonify({'message': 'Proposal created successfully', 'proposal': proposal.to_dict()}), 201
    else:
        return jsonify({'message': 'Invalid proposal description'}), 400

def vote_proposal():
    data = request.get_json()
    proposal_id = data.get('proposal_id')
    if proposal_id and 0 < proposal_id <= len(proposals):
        votes[proposal_id] += 1
        if votes[proposal_id] >= proposal_threshold:
            proposals[proposal_id - 1].status = 'Approved'
        return jsonify({'message': 'Vote recorded', 'votes': votes[proposal_id]}), 200
    else:
        return jsonify({'message': 'Invalid proposal ID'}), 400

def get_proposals():
    return jsonify({'proposals': [proposal.to_dict() for proposal in proposals]}), 200
