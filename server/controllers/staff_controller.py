

from flask import Flask, request, jsonify
from services.staff_service import StaffService

app = Flask(__name__)
staff_service = StaffService('sqlite:///example.db')

@app.route('/staff/<int:staff_id>/status', methods=['PUT'])
def update_staff_status(staff_id):
    new_status = request.json['new_status']
    staff_service.update_staff_status(staff_id, new_status)
    return jsonify({'message': 'Staff status updated successfully'})