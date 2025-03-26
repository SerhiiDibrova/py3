

from flask import jsonify, request
from . import app
from .business_logic import calculate_completion_statistics_business_logic

def calculate_completion_statistics(program_id):
    if not program_id:
        return jsonify({'error': 'Invalid program ID'}), 400
    completion_statistics = calculate_completion_statistics_business_logic(program_id)
    return jsonify({'completion_statistics': completion_statistics}), 200

@app.route('/programs/<program_id>/completion-statistics', methods=['GET'])
def get_completion_statistics(program_id):
    return calculate_completion_statistics(program_id)