

from flask import jsonify
from server.models import Book, Patron

class BookController:
    def update_book_availability(book_id, change):
        book = Book.query.get(book_id)
        new_availability = book.available_copies + change
        book.available_copies = new_availability
        book.save()
        return jsonify({'message': 'Book availability updated successfully'})

    def check_book_availability(book_id):
        book = Book.query.get(book_id)
        return jsonify({'availability': book.available_copies})

    def check_patron_account_status(patron_id):
        patron = Patron.query.get(patron_id)
        return jsonify({'status': patron.status})