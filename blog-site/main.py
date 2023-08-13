import smtplib
import os
import dotenv
from flask import Flask, render_template, redirect, url_for,request,flash
from flask_bootstrap import Bootstrap5
from flask_pymongo import PyMongo
from pymongo import MongoClient
from bson.objectid import ObjectId
from flask_ckeditor import CKEditor
from flask_gravatar import Gravatar
from flask_login import UserMixin, login_user, LoginManager, current_user, logout_user
from functools import wraps
from werkzeug.security import generate_password_hash, check_password_hash
from forms import PostForm,RegisterForm,LoginForm
from datetime import date

dotenv.load_dotenv()


app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
ckeditor = CKEditor(app)
Bootstrap5(app)

def get_database():
   CONNECTION_STRING = os.getenv("MONGO_URI")
   client = MongoClient(CONNECTION_STRING)
   return client['blogposts']
 
dbname = get_database()
post = dbname["posts"]  
user = dbname["users"]

login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return user.find_one({"_id": ObjectId(user_id)})

gravatar = Gravatar(app,
                    size=100,
                    rating='g',
                    default='retro',
                    force_default=False,
                    force_lower=False,
                    use_ssl=False,
                    base_url=None)

class User(UserMixin):
    def __init__(self, user_data):
        self.id = str(user_data["_id"])
        self.email = user_data["email"]
        self.name = user_data["name"]
        self.password = user_data["password"]
        self.posts = user_data.get("posts", [])


    def is_active(self):
        return True 

    def get_id(self):
        return self.id

@login_manager.user_loader
def load_user(user_id):
    user_data = user.find_one({"_id": ObjectId(user_id)})
    if user_data:
        return User(user_data)
    return None


def admin_only(function):
    @wraps(function)
    def wrapper(*args,**kwargs):
        if current_user.is_authenticated and current_user.id == "64d945ff308730b07565983b":
            return function(*args,**kwargs)
        else:
            return redirect(url_for("home"))
    return wrapper


@app.route('/')
def home():
    all_posts = post.find()
    return render_template("index.html", posts=all_posts,current_user=current_user)

@app.route('/about')
def about():
    return render_template("about.html",current_user=current_user)

@app.route('/contact',methods=["GET","POST"])
def contact():
    if request.method == "POST":
        data = request.form
        send_mail(data["name"],data["email"],data["phone"],data["message"])
        return render_template("contact.html",msg_sent=True,current_user=current_user)
    return render_template("contact.html",msg_sent=False,current_user=current_user)

@app.route('/getBlog/<string:id>')
def getBlog(id):
    blog = post.find_one({"_id": ObjectId(id)})
    return render_template("post.html",post=blog,current_user=current_user)

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
        post.insert_one(new_post)
        return redirect(url_for("home"))
    return render_template("make-post.html", form=form,current_user=current_user)

@app.route('/edit-post/<string:id>', methods=["GET", "POST"])
@admin_only
def edit_post(id):
    requested_post = post.find_one({"_id": ObjectId(id)})
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
        post.update_one({"_id": ObjectId(id)}, {"$set": updated_post})
        return redirect(url_for("getBlog", id=id, current_user=current_user))
    return render_template("make-post.html", form=form, is_edit=True,current_user=current_user)

@app.route('/delete/<string:id>')
@admin_only
def delete_post(id):
    post.delete_one({"_id": ObjectId(id)})
    return redirect(url_for("home",current_user=current_user))
@app.route('/register', methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if user.find_one({"email": form.email.data}):
            flash("User already exists")
            return render_template("register.html", form=form)
        new_user = {
            "email": form.email.data,
            "password": generate_password_hash(form.password.data, method="pbkdf2:sha256", salt_length=8),
            "name": form.name.data,
            "posts": []
        }
        user.insert_one(new_user)
        return redirect(url_for("login"))
    return render_template("register.html", form=form, current_user=current_user)


@app.route('/login',methods=["GET","POST"])
def login():
    form = LoginForm()
    if request.method == "POST":
        data = request.form
        user_data = user.find_one({"email":data["email"]})
        if user_data:
            if check_password_hash(user_data["password"],data["password"]):
                user_instance = User(user_data)
                login_user(user_instance)
                return redirect(url_for("home"))
            else:
                flash("Invalid Password")
                return render_template("login.html",form=form,current_user=current_user)
        else:
            flash("User does not exist")
            return render_template("login.html",form=form,current_user=current_user)
    return render_template("login.html",form=form,current_user=current_user)

@app.route('/logout')
def logout():
    logout_user()
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