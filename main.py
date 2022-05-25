from flask import Flask, render_template, redirect, url_for, flash, request, abort
from flask_bootstrap import Bootstrap
from flask_ckeditor import CKEditor
from datetime import date
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user
from forms import CreatePostForm, RegistrationForm, LoginForm, CommentForm
from flask_gravatar import Gravatar
from functools import wraps

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
ckeditor = CKEditor(app)
Bootstrap(app)
gravatar = Gravatar(app,
                    size=250,
                    rating='x',
                    default='retro',
                    force_default=False,
                    force_lower=False,
                    use_ssl=False,
                    base_url=None)

##CONNECT TO DB
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = "login"


##CONFIGURE TABLES
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(250), nullable=False)
    email = db.Column(db.String(250), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    posts = relationship("BlogPost", backref="user")
    comments = relationship("Comment", backref="user")


class BlogPost(db.Model):
    __tablename__ = "blog_post"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), unique=True, nullable=False)
    subtitle = db.Column(db.String(250), nullable=False)
    date = db.Column(db.String(250), nullable=False)
    body = db.Column(db.Text(250), nullable=False)
    img_url = db.Column(db.String(250), nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    post_comments = relationship("Comment", backref="blog_post")


class Comment(db.Model):
    __tablename__ = "comments"
    id = db.Column(db.Integer, primary_key=True)
    comment = db.Column(db.Text(250), nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    post_id = db.Column(db.Integer, db.ForeignKey("blog_post.id"))


# db.create_all()
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


def admin_only(func):
    @wraps(func)
    def wrapper_func(*args, **kwargs):
        if current_user.get_id() is None:
            return redirect(url_for("login"))
        elif current_user.get_id() != "1":
            return abort(403)
        return func(*args, **kwargs)
    return wrapper_func


@app.route('/')
def get_all_posts():
    admin = False
    if current_user.get_id():
        if int(current_user.get_id()) == 1:
            admin = True
    posts = BlogPost.query.all()
    return render_template("index.html", all_posts=posts, admin=admin)


@app.route('/register', methods=["GET", "POST"])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user_existed = User.query.filter_by(email=form.email.data).first()
        if user_existed:
            flash("You've already signed up with that email, log in instead!.")
            return redirect(url_for("login"))
        else:
            user = User(username=form.username.data,
                        email=form.email.data,
                        password=generate_password_hash(form.password.data, "pbkdf2:sha256", 8))
            db.session.add(user)
            db.session.commit()
            login_user(user)
            return redirect(url_for("get_all_posts"))
    return render_template("register.html", form=form)


@app.route('/login', methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                login_user(user, remember=form.remember.data)
                next_page = request.args.get("next")
                return redirect(next_page) if next_page else redirect(url_for("get_all_posts"))
            else:
                flash("Login unsuccessful, please check your password.", "danger")
        else:
            flash("Login unsuccessful, please check your email.")
    return render_template("login.html", form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('get_all_posts'))


@app.route("/post/<int:post_id>", methods=["Get", "POST"])
def show_post(post_id):
    admin = False
    normal_user = False
    form = CommentForm()
    if current_user.get_id():
        if int(current_user.get_id()) == 1:
            admin = True
        else:
            normal_user = True
    if form.validate_on_submit():
        user = User.query.get(int(current_user.get_id()))
        post = BlogPost.query.get(post_id)
        user_comment = Comment(
            comment=form.comment.data,
            user=user,
            blog_post=post
        )
        db.session.add(user_comment)
        db.session.commit()
        return redirect(url_for("show_post", post_id=post_id))
    requested_post = BlogPost.query.get(post_id)
    blog_comments = requested_post.post_comments
    return render_template("post.html", post=requested_post, comments=blog_comments, admin=admin, user=normal_user,
                           form=form)


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/contact")
def contact():
    return render_template("contact.html")


@app.route("/new-post", methods=["GET", "POST"])
@login_required
@admin_only
def add_new_post():
    form = CreatePostForm()
    user = User.query.get(int(current_user.get_id()))
    if form.validate_on_submit():
        new_post = BlogPost(
            title=form.title.data,
            subtitle=form.subtitle.data,
            body=form.body.data,
            img_url=form.img_url.data,
            date=date.today().strftime("%B %d, %Y"),
            user=user
        )
        db.session.add(new_post)
        db.session.commit()
        return redirect(url_for("get_all_posts"))
    return render_template("make-post.html", form=form)


@app.route("/edit-post/<int:post_id>", methods=["GET", "POST"])
@login_required
@admin_only
def edit_post(post_id):
    post = BlogPost.query.get(post_id)
    edit_form = CreatePostForm(
        title=post.title,
        subtitle=post.subtitle,
        img_url=post.img_url,
        body=post.body
    )
    if edit_form.validate_on_submit():
        post.title = edit_form.title.data
        post.subtitle = edit_form.subtitle.data
        post.img_url = edit_form.img_url.data
        post.body = edit_form.body.data
        db.session.commit()
        return redirect(url_for("show_post", post_id=post.id))

    return render_template("make-post.html", form=edit_form)


@app.route("/delete/<int:post_id>")
@login_required
@admin_only
def delete_post(post_id):
    post_to_delete = BlogPost.query.get(post_id)
    db.session.delete(post_to_delete)
    db.session.commit()
    return redirect(url_for('get_all_posts'))


@app.route("/delete_comment/<int:comment_id>")
@login_required
@admin_only
def delete_comment(comment_id):
    comment_to_delete = Comment.query.get(comment_id)
    post_id = comment_to_delete.blog_post.id
    db.session.delete(comment_to_delete)
    db.session.commit()
    return redirect(url_for("show_post", post_id=post_id))


if __name__ == "__main__":
    app.run(host='127.0.1.1', port=5000, debug=True)
