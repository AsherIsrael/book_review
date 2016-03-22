from system.core.model import Model
import re

class User(Model):
	def __init__(self):
		super(User, self).__init__()

	def validate_registration(self, info):
		print "User validate_registration"
		EMAIL_REGEX = re.compile(r'^[a-za-z0-9\.\+_-]+@[a-za-z0-9\._-]+\.[a-za-z]*$')
		name = info['name']
		alias = info['alias']
		email = info['email']
		password = info['password']
		pass_confirm = info['pass_confirm']

		errors = []

		if len(name) < 1:
			errors.append("name cannot be blank")
		elif not name.replace(" ","").isalpha():
			errors.append("name can only contain letters")

		if len(alias) < 1:
			errors.append("alias cannot be blank")
		elif len(alias) < 3:
			erors.append("alias must be longer than 2 characters")

		if len(email) < 1:
			errors.append("email cannot be blank")
		elif not EMAIL_REGEX.match(email):
			errors.append("must enter a valid email")

		if len(password) < 8:
			errors.append("password must be at least 8 characters")
		elif not password == pass_confirm:
			errors.append("password and confirmation must match")

		if errors:
			print errors
			return {'status': False, 'errors': errors}
		else:
			info['password'] = self.bcrypt.generate_password_hash(info['password'])
			print info
			return {'status': True, 'valid_info': info}

	def validate_login(self, info):
		print "User valiadte_login"
		user = self.get_user_by_email(info['email'])
		print user

		if user:
			print "user returned"
			if self.bcrypt.check_password_hash(user[0]['pass_hash'], info['password']):
				print "pass confirmed"
				return user[0]
		return False


	def create_user(self, info):
		print "User create_user"
		add_user_query = "INSERT INTO users (name, alias, email, pass_hash, created_at) VALUES (%s, %s, %s, %s, NOW())"
		content = [info['name'], info['alias'], info['email'], info['password']]
		self.db.query_db(add_user_query, content)
		get_new_user = "SELECT id, alias FROM users ORDER BY id DESC LIMIT 1"
		user = self.db.query_db(get_new_user)
		return user[0]

	def get_user_by_email(self, email):
		print "User get_user_by_email"
		get_user_query = "SELECT id, alias, pass_hash FROM users WHERE email = %s LIMIT 1"
		return self.db.query_db(get_user_query, [email])

	def get_user_by_id(self, id):
		print "User get_user_by_email"
		get_user_query = "SELECT email, name, alias, pass_hash, (SELECT COUNT(reviews.user_id) FROM reviews WHERE reviews.user_id = %s) as review_count FROM users WHERE id = %s"
		return self.db.query_db(get_user_query, [id, id])