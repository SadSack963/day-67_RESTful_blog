from flask import Flask, render_template, jsonify, redirect, url_for, request
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, URL
# https://flask-ckeditor.readthedocs.io/en/latest/basic.html
from flask_ckeditor import CKEditor, CKEditorField
import datetime as dt


# Delete this code:
# Get blog posts from npoint.io
# import requests
# posts = requests.get("https://api.npoint.io/ed99320662742443cc5b").json()

API_KEY = 'tHWGr3hbWTYF48r3zX899XDVSQYFxf5t'
DB_URI = 'sqlite:///posts.db'

app = Flask(__name__)
app.config['SECRET_KEY'] = API_KEY
ckeditor = CKEditor(app)
Bootstrap(app)

# CONNECT TO DB
app.config['SQLALCHEMY_DATABASE_URI'] = DB_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


# CONFIGURE TABLE
class BlogPost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), unique=True, nullable=False)
    subtitle = db.Column(db.String(250), nullable=False)
    date = db.Column(db.String(250), nullable=False)
    body = db.Column(db.Text, nullable=False)
    author = db.Column(db.String(250), nullable=False)
    img_url = db.Column(db.String(250), nullable=False)


# WTForm
class CreatePostForm(FlaskForm):
    title = StringField("Blog Post Title", validators=[DataRequired()])
    subtitle = StringField("Subtitle", validators=[DataRequired()])
    author = StringField("Your Name", validators=[DataRequired()])
    img_url = StringField("Blog Image URL", validators=[DataRequired(), URL()])
    body = CKEditorField("Blog Content", validators=[DataRequired()])
    submit = SubmitField("Submit Post")


@app.route('/')
def get_all_posts():
    # posts = db.session.query(BlogPost).all()
    posts = BlogPost.query.all()
    return render_template("index.html", all_posts=posts)


@app.route("/post/<int:post_id>")
def show_post(post_id):
    # requested_post = db.session.query(BlogPost).get(post_id)
    requested_post = BlogPost.query.get(post_id)
    if requested_post:
        return render_template("post.html", post=requested_post)
    return jsonify(error={"Not Found": "The blog post ID={index} is not in the database!"}), 404


@app.route("/edit-post/<int:post_id>", methods=["GET", "POST"])
def edit_post(post_id):
    post = BlogPost.query.get(post_id)
    form = CreatePostForm(
        title=post.title,
        subtitle=post.subtitle,
        author=post.author,
        img_url=post.img_url,
        body=post.body,
    )
    if form.validate_on_submit():
        # Add new blog to database
        post = BlogPost(
            title=form.title.data,
            subtitle=form.subtitle.data,
            author=form.author.data,
            img_url=form.img_url.data,
            body=form.body.data,
            date=dt.date.today().strftime("%B %d, %Y"),
        )
        db.session.commit()
        return redirect(url_for("get_all_posts"))
    return render_template("edit-post.html", form=form)


@app.route("/new-post/", methods=["GET", "POST"])
def new_post():
    form = CreatePostForm()
    if form.validate_on_submit():
        # Add new blog to database
        post = BlogPost(
            title=form.title.data,
            subtitle=form.subtitle.data,
            author=form.author.data,
            img_url=form.img_url.data,
            body=form.body.data,
            date=dt.date.today().strftime("%B %d, %Y"),
        )
        db.session.add(post)
        db.session.commit()
        return redirect(url_for("get_all_posts"))
    return render_template("make-post.html", form=form)


@app.route("/delete/<int:post_id>")
def delete_post(post_id):
    post = BlogPost.query.get(post_id)
    db.session.delete(post)
    db.session.commit()
    return redirect(url_for("get_all_posts"))


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/contact")
def contact():
    return render_template("contact.html")


if __name__ == "__main__":
    app.run(host='127.0.0.1', port=5007, debug=True)
