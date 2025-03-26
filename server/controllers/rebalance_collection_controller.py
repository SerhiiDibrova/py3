

from flask import jsonify, request
from server.services.rebalance_collection_service import RebalanceCollectionService

class RebalanceCollectionController:
    def handle_request(self):
        data = request.get_json()
        result = RebalanceCollectionService().analyze_and_manage_collections(data)
        return jsonify(result)