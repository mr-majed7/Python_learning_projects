from post import Post
import requests
import smtplib
import os
import dotenv
from flask import Flask, render_template, redirect, url_for,request
from flask_bootstrap import Bootstrap5
from flask_pymongo import PyMongo
from pymongo import MongoClient
from bson.objectid import ObjectId
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

def get_database():
 
   # Provide the mongodb atlas url to connect python to mongodb using pymongo
   CONNECTION_STRING = os.getenv("MONGO_URI")
 
   # Create a connection using MongoClient. You can import MongoClient or use pymongo.MongoClient
   client = MongoClient(CONNECTION_STRING)
 
   # Create the database for our example (we will use the same database throughout the tutorial
   return client['blogposts']
  
# This is added so that many files can reuse the function get_database()
 
dbname = get_database()
collection_name = dbname["posts"]  

# post = {
#     "title": "Exploring the Wonders of Space",
#     "subtitle": "Journey through the cosmos and discover the secrets of the universe.",
#     "date": "7th August 2023",
#     "body": "Breathtaking galaxies, mesmerizing nebulae, and distant planets await the intrepid explorer of space. Gaze through telescopes, study celestial phenomena, and ponder the mysteries of dark matter and black holes. Join us on an astronomical journey beyond our earthly confines. Peer into the heart of Orion's Belt, where stars are born from the cosmic dust of interstellar nurseries. Marvel at the dance of Jupiter's moons as they orbit the giant gas planet, each with its own unique characteristics. Experience the awe of witnessing a solar eclipse, where the moon momentarily conceals the sun, revealing the sun's corona in all its splendor. Embark on a mission to unravel the history of the cosmos, from the Big Bang to the formation of galaxies and the evolution of life. Whether you're a seasoned stargazer or a curious novice, the wonders of space beckon you to explore, learn, and dream.",
#     "author": "Loreweaver Quillspire",
#     "img_url": "https://images.unsplash.com/photo-1559657693-e816ff3bd9af?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1171&q=80"
# }
# collection_name.insert_one(post)

class PostForm(FlaskForm):
    title = StringField("Blog Post Title",validators=[DataRequired()])
    subtitle = StringField("Subtitle",validators=[DataRequired()])
    author = StringField("Author",validators=[DataRequired()])
    img_url = StringField("Image URL",validators=[DataRequired(),URL()])
    body = CKEditorField("Blog Content",validators=[DataRequired()])
    submit = SubmitField("Submit Post")

@app.route('/')
def home():
    all_posts = collection_name.find()
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

@app.route('/getBlog/<string:id>')
def getBlog(id):
    blog = collection_name.find_one({"_id": ObjectId(id)})
    return render_template("post.html",post=blog)

@app.route('/new-post', methods=["GET", "POST"])
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        new_post = {
            "title": form.title.data,
            "subtitle": form.subtitle.data,
            "date": date.today().strftime("%B %d, %Y"),
            "body": form.body.data,
            "author": form.author.data,
            "img_url": form.img_url.data
        }
        collection_name.insert_one(new_post)
        return redirect(url_for("home"))
    return render_template("make-post.html", form=form)

@app.route('/edit-post/<string:id>', methods=["GET", "POST"])
def edit_post(id):
    requested_post = collection_name.find_one({"_id": ObjectId(id)})
    form = PostForm(
        title=requested_post["title"],
        subtitle=requested_post["subtitle"],
        author=requested_post["author"],
        img_url=requested_post["img_url"],
        body=requested_post["body"]
    )
    if form.validate_on_submit():
        updated_post = {
            "title": form.title.data,
            "subtitle": form.subtitle.data,
            "author": form.author.data,
            "img_url": form.img_url.data,
            "body": form.body.data
        }
        collection_name.update_one({"_id": ObjectId(id)}, {"$set": updated_post})
        return redirect(url_for("getBlog", id=id))
    return render_template("make-post.html", form=form, is_edit=True)

@app.route('/delete/<string:id>')
def delete_post(id):
    collection_name.delete_one({"_id": ObjectId(id)})
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