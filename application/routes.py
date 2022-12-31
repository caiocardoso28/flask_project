import application
import os
import secrets
from PIL import Image
from application.models import User, Post
from application import app, db, bcrypt
from flask import render_template, url_for, flash, redirect, request, abort
from application.forms import RegistrationForm, LoginForm, UpdateAccountForm, PostForm, SearchForm
from flask_login import login_user, current_user, logout_user, login_required


@app.route('/', methods=['POST', 'GET'])
def index():
    image_file = url_for('static', filename='MicrosoftTeams-image (2).jpg')
    form = SearchForm()
    if form.validate_on_submit():
        return redirect(url_for('search'))
    video = url_for('static', filename='EXP VIDEO 2022.mp4')
    posts = Post.query.order_by(Post.date_posted.desc()).all()
    return render_template('home.html', title='Home', posts=posts, video=video, len=len, form=form)


@app.route('/login', methods=['POST', 'GET'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            return redirect(url_for('index'))
        else:
            flash('Login Unsuccessful. Please check email and Password', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route('/register/', methods=['POST', 'GET'])
@app.route('/register/<typ>', methods=['POST', 'GET'])
def register(typ):
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = RegistrationForm()

    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(first_name=form.first.data, last_name=form.last.data, username=form.username.data, email=form.email.data, password=hashed_password, type=typ)
        db.session.add(user)
        db.session.commit()
        flash(f'Your account has been created! Log in to finish setting up your {typ} profile.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form, selection=typ)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/selection')
def selection():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    return render_template('selection.html')


def save_picture(form_picture, typ=None):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    if typ == 'media':
        picture_path = os.path.join(app.root_path, 'static/user_uploads', picture_fn)
    else:
        picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)
        output_size = (125, 125)

    i = Image.open(form_picture)
    # resize and save
    bwidth = 600
    ratio = bwidth / float(i.size[0])
    height = int((float(i.size[1]) * ratio))
    i = i.resize((bwidth, height), Image.ANTIALIAS)
    i.save(picture_path)

    return picture_fn


@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('account.html', title='Account',
                           image_file=image_file, form=form)


@app.route("/post/new", methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        if form.content.data:
            media = save_picture(form.content.data, 'media')
        else:
            media = None
        post = Post(title=current_user.username, content=form.title.data, media=media, author=current_user, type='media')
        db.session.add(post)
        db.session.commit()
        flash("Posted successfully", 'success')
        return redirect(url_for('index'))
    return render_template("create_post.html", title="Upload Post", form=form)


@app.route("/post/<int:post_id>")
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', title=post.title, post=post)


@app.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash('Your post has been updated!', 'success')
        return redirect(url_for('post', post_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
    return render_template('create_post.html', title='Update Post',
                           form=form, legend='Update Post')


@app.route("/post/id/<int:post_id>")
def get_post(post_id):
    # post_id = request.args.get('post_id')
    post = Post.query.get_or_404(int(post_id))

    return render_template("post.html", title=f"{post.author.username} - Post", post=post)


@app.route("/profile/id/<int:user_id>")
def profile(user_id):
    # post_id = request.args.get('post_id')
    user = User.query.get_or_404(int(user_id))

    return render_template("profile.html", title=f"{user.username} - Profile", user=user, len=len)


@app.route("/post/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('index'))


@app.route("/search/<searched>")
def search(searched):

    return render_template("search.html")


@app.route("/test")
def test():

    return render_template("test.html")



