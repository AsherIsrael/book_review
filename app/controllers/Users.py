from system.core.controller import *

class Users(Controller):
	def __init__(self, action):
		super(Users, self).__init__(action)
		self.load_model('User')

	def index(self):
		return self.load_view('/users/index.html')

	def registration(self):
		print "Users registration"
		info = {
			'name': request.form['name'],
			'alias': request.form['alias'],
			'email': request.form['email'],
			'password': request.form['password'],
			'pass_confirm': request.form['pass_confirm']
		}

		result = self.models['User'].validate_registration(info)

		if result['status']:
			user = self.models['User'].create_user(result['valid_info'])
			session['id'] = user['id']
			session['alias'] = user['alias']
			return redirect("/books")
		else:
			for error in result['errors']:
				flash(error)
			return redirect('/')

	def login(self):
		print "Users login"
		info = {
			'email': request.form['email'],
			'password': request.form['password']
		}

		result = self.models['User'].validate_login(info)

		if result:
			session['id'] = result['id']
			session['alias'] = result['alias']
			return redirect('/books')
		else:
			flash("incorrect email or password")
			return redirect('/')