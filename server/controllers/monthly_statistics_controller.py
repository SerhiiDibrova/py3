

from flask import Blueprint, request, jsonify
from server.services.monthly_statistics_service import generate_monthly_statistics

monthly_statistics_controller = Blueprint('monthly_statistics_controller', __name__)

@monthly_statistics_controller.route('/generate_monthly_statistics', methods=['POST'])
def generate_monthly_statistics_endpoint():
    p_year = request.json['p_year']
    p_month = request.json['p_month']
    generate_monthly_statistics(p_year, p_month)
    return jsonify({'message': 'Monthly statistics generated successfully'})