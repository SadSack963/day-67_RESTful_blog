from flask import Flask, render_template, jsonify, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, URL
from flask_ckeditor import CKEditor, CKEditorField


# Delete this code:
# Get blog posts from npoint.io
# import requests
# posts = requests.get("https://api.npoint.io/ed99320662742443cc5b").json()

app = Flask(__name__)
app.config['SECRET_KEY'] = 'tHWGr3hbWTYF48r3zX899XDVSQYFxf5t'
ckeditor = CKEditor(app)
Bootstrap(app)

# CONNECT TO DB
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///posts.db'
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
    body = StringField("Blog Content", validators=[DataRequired()])
    submit = SubmitField("Submit Post")


# Get blog posts from database
posts = db.session.query(BlogPost).all()


@app.route('/')
def get_all_posts():
    return render_template("index.html", all_posts=posts)


@app.route("/post/<int:index>")
def show_post(index):
    # requested_post = None  # Not required when using the return in the if statement
    for blog_post in posts:
        # id is a Class property - not a dictionary subscript!
        # if blog_post["id"] == index:  # TypeError: 'BlogPost' object is not subscriptable
        if blog_post.id == index:
            requested_post = blog_post
            return render_template("post.html", post=requested_post)
    return jsonify(error={"Not Found": "The blog post ID={index} is not in the database!"}), 404


@app.route("/edit-post/<int:post_id>")
def edit_post(post_id):
    return render_template("edit-post.html")


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/contact")
def contact():
    return render_template("contact.html")


if __name__ == "__main__":
    app.run(host='127.0.0.1', port=5007, debug=True)
