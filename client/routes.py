

from flask import Blueprint, request, jsonify
from .controllers.book_review_controller import BookReviewController

book_review_blueprint = Blueprint('book_review', __name__)

@book_review_blueprint.route('/add_book_review', methods=['POST'])
def add_book_review():
    book_id = request.json['book_id']
    patron_id = request.json['patron_id']
    rating = request.json['rating']
    review_text = request.json['review_text']
    controller = BookReviewController()
    result = controller.add_book_review(book_id, patron_id, rating, review_text)
    return jsonify({'result': result})