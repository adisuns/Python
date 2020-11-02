import os, secrets
from PIL import Image
from sqlalchemy import desc
from flask import render_template, url_for, flash, redirect, request, abort
from flaskblog import app, db, bcrypt, mail
from flaskblog.forms import RegistrationForm, LoginForm, UpdateAccount, UpdatePassword, PostForm, RequestRestForm
from flaskblog.models import User, Post
from flask_login import login_user, current_user, logout_user, login_required
from flask_mail import Message


@app.route("/")  # route is example of decorator; / is route of the site
@app.route("/home")
def home():
    page = request.args.get('page', 1, type=int)  # 1 is default page number
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
    return render_template('index.html', posts=posts)


@app.route("/about")  # about route
def about():
    return render_template('about-us.html', title='About')


@app.route("/register", methods=['GET', 'POST'])  # added get and post method for registration forms
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f'Account created for {form.username.data} ', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


# check if user passowrd is correct
def check_password(form_password):
    if bcrypt.check_password_hash(current_user.password, form_password.data):
        return True


@app.route("/login", methods=['GET', 'POST'])  # login route
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')  # it gets next param; eg http://127.0.0.1:5000/login?next=%2Fedit ;
            # it will redirect login page, log in the user and then redirect user to requested page; next param
            return redirect(next_page) if next_page else redirect(url_for('dashboard'))
        else:
            flash("Invalid credentials, please try again", 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route("/logout")  # logout route
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)  # as we are not going to use file name, we have used _
    picture_filename = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/images', picture_filename)
    picture_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(picture_size)
    i.save(picture_path)
    i.save(picture_path)
    return picture_filename


@app.route("/update_account", methods=['GET', 'POST'])  # logout route
@login_required
def update_account():
    form = UpdateAccount()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated', 'success')
        return redirect(url_for('update_account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename='images/' + current_user.image_file)
    return render_template('update_account.html', title='Edit Profile', image_file=image_file, form=form)


@app.route("/password", methods=['GET', 'POST'])  # logout routepassword
@login_required
def password():
    form = UpdatePassword()
    image_file = url_for('static', filename='images/' + current_user.image_file)
    if form.validate_on_submit():
        if bcrypt.check_password_hash(current_user.password, form.current_password.data):
            hashed_password = bcrypt.generate_password_hash(form.new_password.data).decode('utf-8')
            current_user.password = hashed_password
            db.session.commit()
            flash("Your password is updated, Please login again", 'success')
            logout_user()
            return redirect(url_for('home'))
    else:
        return render_template('password.html', title='Update Password', image_file=image_file, form=form)


@app.route("/post/new", methods=['GET', 'POST'])  # logout routepassword
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, content=form.content.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your post has been added successfully', 'success')
        return redirect(url_for('home'))
    else:
        return render_template('add_post.html', title='New Post', form=form, legend='New Post')


@app.route("/post/<int:post_id>", methods=['GET', 'POST'])  # logout routepassword
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', title=post.title, post=post)


@app.route("/post/<int:post_id>/update", methods=['GET', 'POST'])  # logout routepassword
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        print("form is validated and submited")
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash("your post is updated", 'success')
        return redirect(url_for('post', post_id=post.id))
    elif request.method == 'GET':
        print("form is not submited")
        form.title.data = post.title
        form.content.data = post.content
        print(form)
        return render_template('add_post.html', title='Update Post', form=form, legend='Update Post')


@app.route("/myaccount/posts", methods=['GET', 'POST'])  # logout routepassword
@login_required
def myposts():
    page = request.args.get('page', 1, type=int)  # 1 is default page number
    posts = Post.query.filter_by(user_id=current_user.id).order_by(desc(Post.date_posted)).paginate(page=page,
                                                                                                    per_page=5)
    return render_template('myaccount_posts.html', posts=posts)


@app.route("/post/<int:post_id>/delete", methods=['POST'])  # logout routepassword
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('post has been deleted', 'success')
    return redirect(url_for('home'))


@app.route("/user/<string:username>")  # logout routepassword
def user_profile(username):
    user = User.query.filter_by(username=username).first_or_404()
    post_count = Post.query.filter_by(user_id=user.id).count()
    return render_template('user_profile.html', user=user, post_count=post_count)


@app.route("/dashboard")  # logout routepassword
@login_required
def dashboard():
    user = current_user
    post_count = Post.query.filter_by(user_id=user.id).count()
    return render_template('dashboard.html', user=user, post_count=post_count)


@app.route("/user/<string:username>/posts")  # logout routepassword
def user_posts(username):
    user = User.query.filter_by(username=username).first_or_404()
    page = request.args.get('page', 1, type=int)  # 1 is default page number
    posts = Post.query.filter_by(author=user).order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
    return render_template('user_posts.html', user=user, posts=posts)


def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request', sender='noreply@demo.com', recipients=[user.email])
    msg.body = f'''To reset your password, visit the following link:
{url_for('reset_token', token=token, _external=True)}
If you did not make this request then simply ignore this email and no changes will be made.
'''
    mail.send(msg)


@app.route("/reset_password/", methods=['GET', 'POST'])  # logout routepassword
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RequestRestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('email has been send with password reset info', 'info')
        return redirect(url_for('login'))
    return render_template('reset_request.html', title='Rest Request', form=form)


@app.route("/reset_password/<token>", methods=['GET', 'POST'])  # logout routepassword
@login_required
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    user = User.verify_token(token)
    if user is None:
        flash('token has been expired', 'warning')
        return redirect(url_for('reset_request'))
    form = UpdatePassword()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash('passwowrd has been updated', 'success')
        return redirect(url_for('login'))
    return render_template('password.html', title='Update Password', form=form)
