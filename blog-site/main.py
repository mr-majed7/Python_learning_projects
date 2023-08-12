from post import Post
import requests
import smtplib
import os
import dotenv
from flask import Flask, render_template, redirect, url_for,request
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, URL
from flask_ckeditor import CKEditor, CKEditorField
from datetime import date

dotenv.load_dotenv()


app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap5(app)
ckeditor = CKEditor(app)

# CONNECT TO DB
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///posts.db'
db = SQLAlchemy()
db.init_app(app)


# CONFIGURE TABLE
class BlogPost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), unique=True, nullable=False)
    subtitle = db.Column(db.String(250), nullable=False)
    date = db.Column(db.String(250), nullable=False)
    body = db.Column(db.Text, nullable=False)
    author = db.Column(db.String(250), nullable=False)
    img_url = db.Column(db.String(250), nullable=False)


with app.app_context():
    db.create_all()

class PostForm(FlaskForm):
    title = StringField("Blog Post Title",validators=[DataRequired()])
    subtitle = StringField("Subtitle",validators=[DataRequired()])
    author = StringField("Author",validators=[DataRequired()])
    img_url = StringField("Image URL",validators=[DataRequired(),URL()])
    body = CKEditorField("Blog Content",validators=[DataRequired()])
    submit = SubmitField("Submit Post")

@app.route('/')
def home():
    all_posts = db.session.execute(db.select(BlogPost)).scalars()
    return render_template("index.html", posts=all_posts)

@app.route('/about')
def about():
    return render_template("about.html")
@app.route('/contact',methods=["GET","POST"])
def contact():
    if request.method == "POST":
        data = request.form
        send_mail(data["name"],data["email"],data["phone"],data["message"])
        return render_template("contact.html",msg_sent=True)
    return render_template("contact.html",msg_sent=False)

@app.route('/getBlog/<int:id>')
def getBlog(id):
    blog = db.session.execute(db.select(BlogPost).where(BlogPost.id == id)).scalar()
    return render_template("post.html",post=blog)

@app.route('/new-post',methods=["GET","POST"])
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        new_post = BlogPost(
            title = form.title.data,
            subtitle = form.subtitle.data,
            date = date.today().strftime("%B %d, %Y"),
            body = form.body.data,
            author = form.author.data,
            img_url = form.img_url.data
        )
        db.session.add(new_post)
        db.session.commit()
        return redirect(url_for("home"))
    return render_template("make-post.html",form=form)

@app.route('/edit-post/<int:id>',methods=["GET","POST"])
def edit_post(id):
    requested_post = db.session.execute(db.select(BlogPost).where(BlogPost.id == id)).scalar()
    form = PostForm(
        title = requested_post.title,
        subtitle = requested_post.subtitle,
        author = requested_post.author,
        img_url = requested_post.img_url,
        body = requested_post.body
    )
    if form.validate_on_submit():
        requested_post.title = form.title.data
        requested_post.subtitle = form.subtitle.data
        requested_post.author = form.author.data
        requested_post.img_url = form.img_url.data
        requested_post.body = form.body.data
        db.session.commit()
        return redirect(url_for("getBlog",id=id))
    return render_template("make-post.html",form=form,is_edit=True)

@app.route('/delete/<int:id>')
def delete_post(id):
    post_to_delete = db.session.execute(db.select(BlogPost).where(BlogPost.id == id)).scalar()
    db.session.delete(post_to_delete)
    db.session.commit()
    return redirect(url_for("home"))

def send_mail(name,email,phone,message):
    my_email = os.getenv("OWNER_EMAIL")
    password = os.getenv("APP_PASSWORD")
    with smtplib.SMTP("smtp.gmail.com") as connection:
        connection.starttls()
        connection.login(user=my_email,password=password)
        connection.sendmail(from_addr=my_email,to_addrs=email,msg=f"Subject:New Message\n\nName: {name}\nEmail: {email}\nPhone: {phone}\nMessage: {message}")


if __name__ == "__main__":
    app.run(debug=True)




# https://www.npoint.io/docs/fccebc96ef732973b267