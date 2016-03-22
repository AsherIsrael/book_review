from system.core.model import Model

class Author(Model):
	def __init__(self):
		super(Author, self).__init__()

	def get_all_authors(self):
		get_all_author_query = "SELECT * FROM authors ORDER BY name"
		return self.db.query_db(get_all_author_query)

	def get_author(self, name):
		get_author_query = "SELECT * FROM authors WHERE name = %s"
		return self.db.query_db(get_author_query, [name])

	def check_for_author(self, name):
		check_author_query = "SELECT id FROM authors WHERE name = %s"
		return self.db.query_db(check_author_query, [name])

	def add_author(self, name):
		add_author_query = "INSERT INTO authors (name, created_at) VALUES (%s, NOW())"
		self.db.query_db(add_author_query, [name])
		last_author = "SELECT id FROM authors ORDER BY id DESC LIMIT 1"
		return self.db.query_db(last_author)