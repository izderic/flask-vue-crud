import os
import uuid

import stripe
from flask import Flask, jsonify, request
from flask_cors import CORS


# configuration
DEBUG = True

# instantiate the app
app = Flask(__name__)
app.config.from_object(__name__)

# enable CORS
CORS(app)

BOOKS = [
    {
        'id': uuid.uuid4().hex,
        'title': 'On the Road',
        'author': 'Jack Kerouac',
        'read': True,
        'price': '19.99'
    },
    {
        'id': uuid.uuid4().hex,
        'title': 'Harry Potter and the Philosopher\'s Stone',
        'author': 'J. K. Rowling',
        'read': False,
        'price': '9.99'
    },
    {
        'id': uuid.uuid4().hex,
        'title': 'Green Eggs and Ham',
        'author': 'Dr. Seuss',
        'read': True,
        'price': '3.99'
    },
    {
        'id': uuid.uuid4().hex,
        'title': 'Clean Code',
        'author': 'Robert C. Martin',
        'read': False,
        'price': '39.99'
    },
    {
        'id': uuid.uuid4().hex,
        'title': 'Django by Example',
        'author': 'Antonio Melé',
        'read': True,
        'price': '44.99'
    }
]


# Utils

def find_book(book_id):
    book_filter = list(filter(lambda book: book['id'] == book_id, BOOKS))
    if book_filter:
        return book_filter[0]


def book_exists(title, author, book_id=None):
    for book in BOOKS:
        if (book_id is None or book_id != book['id']) and book['title'] == title and book['author'] == author:
            return True
    return False


def remove_book(book_id):
    for book in BOOKS:
        if book['id'] == book_id:
            BOOKS.remove(book)
            return True
    return False


# Routes

# sanity check route
@app.route('/ping', methods=['GET'])
def ping_pong():
    return jsonify('pong!')


@app.route('/books', methods=['GET', 'POST'])
def all_books():
    response_object = {'status': 'success'}
    if request.method == 'POST':
        post_data = request.get_json()

        title = post_data['title']
        author = post_data['author']

        # Check if other book with the same title and author exists.
        if book_exists(title, author):
            return jsonify({'status': 'error', 'message': 'Book with title %s and author %s already exists' % (title, author)}), 404

        BOOKS.append({
            'id': uuid.uuid4().hex,
            'title': post_data.get('title'),
            'author': post_data.get('author'),
            'read': post_data.get('read'),
            'price': post_data.get('price')
        })
        response_object['message'] = 'Book added!'
    else:
        response_object['books'] = BOOKS
    return jsonify(response_object)


@app.route('/books/<book_id>', methods=['GET', 'PUT', 'DELETE'])
def single_book(book_id):
    response_object = {'status': 'success'}
    if request.method == 'GET':
        response_object['book'] = find_book(book_id)
    if request.method == 'PUT':
        post_data = request.get_json()

        title = post_data.get('title')
        author = post_data.get('author')

        # Check if other book with the same title and author exists.
        if title and author and book_exists(title, author, book_id=book_id):
            return jsonify({'status': 'error', 'message': 'Book with title %s and author %s already exists' % (title, author)}), 404

        # Update the book data.
        for book in BOOKS:
            if book_id == book['id']:
                book.update(post_data)
                break

        response_object['message'] = 'Book updated!'
    if request.method == 'DELETE':
        remove_book(book_id)
        response_object['message'] = 'Book removed!'
    return jsonify(response_object)


@app.route('/charge', methods=['POST'])
def create_charge():
    post_data = request.get_json()
    amount = round(float(post_data.get('book')['price']) * 100)
    stripe.api_key = os.environ.get('STRIPE_SECRET_KEY')
    charge = stripe.Charge.create(
        amount=amount,
        currency='usd',
        card=post_data.get('token'),
        description=post_data.get('book')['title']
    )
    response_object = {
        'status': 'success',
        'charge': charge
    }
    return jsonify(response_object), 200


@app.route('/charge/<charge_id>')
def get_charge(charge_id):
    stripe.api_key = os.environ.get('STRIPE_SECRET_KEY')
    response_object = {
        'status': 'success',
        'charge': stripe.Charge.retrieve(charge_id)
    }
    return jsonify(response_object), 200


if __name__ == '__main__':
    app.run()
