

from .repository.book_review_repository import BookReviewRepository

class BookReviewController:
    def __init__(self):
        self.repository = BookReviewRepository()

    def add_book_review(self, book_id, patron_id, rating, review_text):
        if book_id is None or patron_id is None or rating is None or review_text is None:
            raise Exception('Invalid input parameters')
        self.repository.insert_book_review(book_id, patron_id, rating, review_text)
        return 'Review added successfully'