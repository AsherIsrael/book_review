from system.core.controller import *

class Books(Controller):
	def __init__(self, action):
		super(Books, self).__init__(action)
		self.load_model('Book')
		self.load_model('Author')
		self.load_model('Review')

	def index(self):
		print "Books index"
		recent_reviews = self.models['Review'].get_most_recent_reviews()
		books = self.models['Book'].get_all_books()
		return self.load_view('/books/index.html', books=books, recent_reviews=recent_reviews)

	def add(self):
		authors = self.models['Author'].get_all_authors()
		return self.load_view('/books/book_add.html', authors=authors)

	def new(self):
		errors = []
		new_author = request.form['new_author']
		if new_author:
			if not self.models['Author'].check_for_author(new_author):
				print "author not found"
				author_id = self.models['Author'].add_author(new_author)[0]
			else:
				print "new author in database"
				author_id = self.models['Author'].get_author(new_author)[0]['id']
		else:
			author_id = request.form['author']
		info = {
			'title': request.form['title'],
			'author_id': author_id,
			'review': request.form['review'],
			'rating': request.form['rating']
		}
		print author_id

		valid_title = self.models['Book'].validate_book_title(info['title'])
		valid_review = self.models['Review'].validate_review(info['review'])
		if valid_title:
			errors.append(valid_title)
		if valid_review:
			errors.append(valid_review)


		if not errors:
			new_book = self.models['Book'].add_book(info)
			book_id = new_book['id']
			info['book_id'] = book_id
			info['user_id'] = session['id']
			return self.post_review(info)
		else:
			for error in errors:
				flash(error)
			print "errors found"
			return redirect('/add')

	def new_review(self):
		print "Books new_review"
		info = {
			'review': request.form['review'],
			'rating': request.form['rating'],
			'book_id': request.form['book_id'],
			'user_id': session['id']
		}

		return self.post_review(info)

	def post_review(self, info):
		print "Books post_review"
		print info
		review = info['review']
		result = self.models['Review'].validate_review(review)

		if result:
			flash(result)
		else:
			self.models['Review'].new_review(info)
		return redirect('/books/'+str(info['book_id']))

	def books(self, id):
		book = self.models['Book'].get_book(id)[0]
		print book
		if not book:
			return redirect('/books')
		reviews = self.models['Review'].get_book_reviews(id)
		return self.load_view('/books/book_page.html', book=book, reviews=reviews)

	def delete_review(self, id):
		book_id = self.models['Review'].delete_review(id)[0]['book_id']
		return redirect('/books/'+str(book_id))