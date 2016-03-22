from system.core.model import Model

class Review(Model):
	def __init__(self):
		super(Review, self).__init__()

	def new_review(self, info):
		new_review_query = "INSERT INTO reviews (content, user_id, book_id, rating, created_at) VALUES (%s, %s, %s, %s, NOW())"
		content = [info['review'], info['user_id'], info['book_id'], info['rating']]
		return self.db.query_db(new_review_query, content)

	def validate_review(self, review):
		if len(review) < 1:
			return "review cannot be blank"
		else:
			return False

	def get_book_reviews(self, book_id):
		get_reviews_query = "SELECT users.alias, users.id as user_id, reviews.id, reviews.content, reviews.created_at, reviews.rating FROM reviews JOIN users ON reviews.user_id = users.id WHERE reviews.book_id = %s ORDER BY reviews.created_at DESC"
		return self.db.query_db(get_reviews_query, [book_id])

	def get_user_reviews(self, user_id):
		get_reviews_query = "SELECT books.title, books.id FROM books JOIN reviews ON reviews.book_id = books.id JOIN users ON users.id = reviews.user_id WHERE reviews.user_id = %s ORDER BY books.title"
		return self.db.query_db(get_reviews_query, [user_id])

	def get_most_recent_reviews(self):
		get_reviews_query = "SELECT books.title, books.id as book_id, reviews.rating, reviews.content, reviews.created_at, users.id as user_id, users.alias FROM books JOIN reviews ON reviews.book_id = books.id JOIN users ON users.id = reviews.user_id ORDER BY reviews.created_at DESC LIMIT 3"
		return self.db.query_db(get_reviews_query)

	def delete_review(self, id):
		removed_review_query = "SELECT book_id FROM reviews WHERE id = %s"
		removed_review_book = self.db.query_db(removed_review_query, [id])
		delete_review_query = "DELETE FROM reviews WHERE id = %s"
		self.db.query_db(delete_review_query, [id])
		return removed_review_book