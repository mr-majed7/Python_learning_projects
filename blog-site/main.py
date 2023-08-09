from flask import Flask, render_template
from post import Post
import requests


app = Flask(__name__)

posts = requests.get("https://api.npoint.io/c790b4d5cab58020d391").json()
post_objects = []
for post in posts:
    post_obj = Post(post["id"], post["title"], post["subtitle"], post["body"])
    post_objects.append(post_obj)

@app.route('/')
def home():
    return render_template("index.html",blogs=post_objects)

@app.route('/getBlog/<id>')
def getBlog(id):
    for blog in post_objects:
        if blog.id == int(id):
            return render_template("post.html",blog=blog)
    return render_template("post.html",blog=None)

if __name__ == "__main__":
    app.run(debug=True)

