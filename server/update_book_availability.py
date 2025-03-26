

from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///books.db'
db = SQLAlchemy(app)

class Books(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    available_copies = db.Column(db.Integer, nullable=False)

def update_book_availability(book_id, change):
    book = Books.query.get(book_id)
    if book:
        new_availability = book.available_copies + change
        book.available_copies = new_availability
        db.session.commit()
        return jsonify({'message': 'Book availability updated successfully'}), 200
    else:
        return jsonify({'message': 'Book not found'}), 404

@app.route('/update-book-availability/<int:book_id>/<int:change>', methods=['PUT'])
def update_book_availability_route(book_id, change):
    return update_book_availability(book_id, change)

if __name__ == '__main__':
    app.run(debug=True)