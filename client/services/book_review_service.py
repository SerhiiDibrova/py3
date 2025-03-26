

from flask import current_app
from ..models import BookReview, db

class BookReviewService:
    def add_book_review(self, book_id, patron_id, rating, review_text):
        if book_id is None or patron_id is None or rating is None or review_text is None:
            raise ValueError('Invalid input parameters')
        book_review = BookReview(book_id, patron_id, rating, review_text)
        db.session.add(book_review)
        db.session.commit()