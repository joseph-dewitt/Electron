from app import app
from app import db
from app.forms import LoginForm, RegistrationForm, EditProfileForm, PostForm, ResetPasswordRequestForm, ResetPasswordForm
from app.models import User, Post
from app.email import send_password_reset_email
from datetime import datetime
from flask import render_template, flash, redirect, request, url_for
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse

@app.before_request
def before_request():
	if current_user.is_authenticated:
		current_user.last_seen = datetime.utcnow()
		db.session.commit()

@app.route('/', methods = ['GET', 'POST'])
@app.route('/index', methods = ['GET', 'POST'])
@login_required
def index():
	posts = Post.query.all()
	form = PostForm()
	if form.validate_on_submit():
		post = Post(body = form.post.data, author=current_user)
		db.session.add(post)
		db.session.commit()
		flash('Your post is live!')
		return redirect(url_for('index'))
	return render_template(
		'index.html',
		title = 'Welcome!',
		posts = posts,
		form = form)

@app.route('/explore')
@login_required
def explore():
	posts = Post.query.order_by(Post.timestamp.desc()).all()
	return render_template(
		'index.html',
		title='Explore',
		posts=posts)

@app.route('/login', methods = ['GET', 'POST'])
def login():
	if current_user.is_authenticated:
		return redirect(url_for('index'))
	form = LoginForm()
	if form.validate_on_submit():
		user = User.query.filter_by(username=form.username.data).first()
		if user is None or not user.check_password(form.password.data):
			flash('Invalid username or password')
			return redirect(url_for('login'))
		login_user(user, remember=form.remember_me.data)
		next_page = request.args.get('next')
		if not next_page or url_parse(next_page).netloc != '':
			next_page = url_for('index')
		return redirect(next_page)
	return render_template(
		'login.html',
		title = 'Sign In',
		form = form)

@app.route('/logout')
def logout():
	logout_user()
	return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route('/user/<username>')
@login_required
def user(username):
	user = User.query.filter_by(username=username).first_or_404()
	posts = Post.query.filter_by(user_id=user.id)
	return render_template('user.html', user=user, posts=posts)

@app.route('/edit-profile', methods = ['GET', 'POST'])
@login_required
def edit_profile():
	form = EditProfileForm(current_user.username)
	if form.validate_on_submit():
		current_user.username = form.username.data
		current_user.about_me = form.about_me.data
		db.session.commit()
		flash('Your changes have been saved.')
		return redirect(url_for('edit_profile'))
	elif request.method == 'GET':
		form.username.data = current_user.username
		form.about_me.data = current_user.about_me
	return render_template('edit_profile.html', title='Edit Profile', form=form)

@app.route('/follow/<username>', methods = ['POST'])
@login_required
def follow_user():
	user = User.query.filter_by(username=username).first()
	if user is None:
		flash("User {} not found").format(username)
		return redirect(url_for('index'))
	if current_user.is_following(user):
		flash("You're already following that user!")
		return redirect(url_for('user', username=username))
	current_user.follow(user)
	db.session.commit()
	flash("You are now following {}!").format(username)
	return redirect(url_for('user', username=username))

@app.route('/unfollow/<username>', methods = ['POST'])
@login_required
def unfollow_user():
	user = User.query.filter_by(username=username).first()
	if user is None:
		flash("User {} not found").format(username)
		return redirect(url_for('index'))
	current_user.unfollow(user)
	db.session.commit()
	flash("You are not following {}!").format(username)
	return redirect(url_for('user', username=username))

@app.route('/request-password-reset', methods = ['GET', 'POST'])
def reset_password_request():
	if current_user.is_authenticated:
		return redirect(url_for('index'))
	form = ResetPasswordRequestForm()
	if form.validate_on_submit():
		user = User.query.filter_by(email=form.email.data).first()
		if user:
			send_password_reset_email(user)
		flash("Check your email for password reset instructions.")
		return redirect(url_for('login'))
	return render_template('reset_password_request.html', title='Reset Password', form=form)

@app.route('/reset-password/<token>', methods=['GET', 'POST'])
def reset_password(token):
	if current_user.is_authenticated:
		return redirect(url_for('index'))
	user = User.verify_reset_password_token(token)
	if not user:
		return redirect(url_for('index'))
	form = ResetPasswordForm()
	if form.validate_on_submit():
		user.set_password(form.password.data)
		db.session.commit()
		flash('Your password has been changed.')
		return redirect(url_for('index'))
	return render_template('reset_password.html', form=form)



# @app.route('/arduino')
# def arduino(message):

