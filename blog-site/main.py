from flask import Flask, render_template
from post import Post
import requests


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

@app.route('/contact')
def contact():
    return render_template("contact.html")

@app.route('/getBlog/<int:id>')
def getBlog(id):
    for post in post_objects:
        if post.id == int(id):
            return render_template("post.html",post=post)
    return render_template("post.html",blog=None)

if __name__ == "__main__":
    app.run(debug=True)




# https://www.npoint.io/docs/fccebc96ef732973b267