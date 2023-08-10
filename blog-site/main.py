from flask import Flask, render_template,request
from post import Post
import requests
import smtplib
import os
import dotenv

dotenv.load_dotenv()


app = Flask(__name__)

posts = requests.get("https://api.npoint.io/fccebc96ef732973b267").json()
post_objects = []
for post in posts:
    post_obj = Post(post["id"], post["title"], post["subtitle"], post["body"],post["author"],post["date"],post["image"])
    post_objects.append(post_obj)

@app.route('/')
def home():
    return render_template("index.html",posts=post_objects)

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
    for post in post_objects:
        if post.id == int(id):
            return render_template("post.html",post=post)
    return render_template("post.html",blog=None)

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