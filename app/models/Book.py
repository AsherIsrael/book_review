from system.core.model import Model

class Book(Model):
	def __init__(self):
		super(Book, self).__init__()

	def validate_book_title(self, title):
		if len(title) < 1:
			return "title cannot be blank"
		else:
			return False

	def add_book(self, info):
		add_book_query = "INSERT INTO books (title, author_id, created_at) VALUES (%s, %s, NOW())"
		content = [info['title'], info['author_id']]
		print content
		self.db.query_db(add_book_query, content)
		new_book = self.db.query_db("SELECT * FROM books ORDER BY id DESC LIMIT 1")[0]
		return new_book

	def get_book(self, id):
		get_book_query = "SELECT books.id, books.title, authors.name as author_name FROM books JOIN authors ON books.author_id = authors.id WHERE books.id = %s"
		return self.db.query_db(get_book_query, [id])

	def get_all_books(self):
		get_books_query = "SELECT books.title, books.id FROM books"
		return self.db.query_db(get_books_query)