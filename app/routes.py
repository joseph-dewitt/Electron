from flask import render_template
from app import app

@app.route('/')
@app.route('/index')
def index():
	user = {'username':'Diana'}
	posts = [
		{
			'author': {'username': 'Joseeeeeeph'},
			'body': 'Beautiful day in Portland!'
		},
		{
			'author': {'username': 'Susan'},
			'body': 'The Avengers movie was so cool!'
		}
	]
	return render_template(
		'index.html',
		title = 'Welcome!',
		user = user,
		posts = posts)
