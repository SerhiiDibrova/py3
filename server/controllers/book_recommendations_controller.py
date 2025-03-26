

from flask import Blueprint, request, jsonify
from server.models import Patron, Book, Loan
from server.repositories import PatronRepository, BookRepository, LoanRepository
from server.services import PatronService, BookService, LoanService

book_recommendations_controller = Blueprint('book_recommendations_controller', __name__)

@book_recommendations_controller.route('/generate_book_recommendations', methods=['GET'])
def generate_book_recommendations():
    patron_id = request.args.get('patron_id')
    patron_service = PatronService(PatronRepository(Patron), BookRepository(Book), LoanRepository(Loan))
    recommended_books = patron_service.generate_book_recommendations(patron_id)
    return jsonify(recommended_books)

class PatronService:
    def __init__(self, patron_repository, book_repository, loan_repository):
        self.patron_repository = patron_repository
        self.book_repository = book_repository
        self.loan_repository = loan_repository

    def generate_book_recommendations(self, patron_id):
        patron_reading_history = self.patron_repository.get_reading_history(patron_id)
        patron_preferences = self.patron_repository.get_preferences(patron_id)
        book_scores = self.calculate_book_scores(patron_reading_history, patron_preferences)
        recommended_books = self.get_recommended_books(book_scores)
        return recommended_books

    def calculate_book_scores(self, patron_reading_history, patron_preferences):
        book_scores = {}
        for book in self.book_repository.get_all_books():
            score = 0
            for loan in patron_reading_history:
                if loan.book_id == book.id:
                    score += 1
            for preference in patron_preferences:
                if preference.book_id == book.id:
                    score += 1
            book_scores[book.id] = score
        return book_scores

    def get_recommended_books(self, book_scores):
        recommended_books = []
        for book_id, score in book_scores.items():
            if score > 0:
                book = self.book_repository.get_book(book_id)
                recommended_books.append(book)
        return recommended_books