from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
import requests


app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap5(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///top-movies.db'
db = SQLAlchemy(app)

class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), unique=True, nullable=False)
    year = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String(250))
    rating = db.Column(db.Float)
    ranking = db.Column(db.Integer)
    review = db.Column(db.String(250))
    img_url = db.Column(db.String(250), unique=True, nullable=False)

with app.app_context():
    db.create_all()

# with app.app_context():
#     new_movie = Movie(
#         title="The Godfather",
#         year=1972,
#         description="An organized crime dynasty's aging patriarch transfers control of his clandestine empire to his reluctant son.",
#         rating=9.7,
#         ranking=1,
#         review="I'm gonna make him an offer he can't refuse.",
#         img_url="https://www.imdb.com/title/tt0068646/mediaviewer/rm1466922497/?ref_=tt_ov_i"
#     )

# with app.app_context():
#     db.session.add(new_movie)
#     db.session.commit()

# with app.app_context():
#     new_movie = Movie(
#         title="Twelve Angry Men",
#         year=1957,
#         description="A jury holdout attempts to prevent a miscarriage of justice by forcing his colleagues to reconsider the evidence.",
#         rating=9.4,
#         ranking=2,
#         review="Life is in their hands -- Death is on their minds!",
#         img_url="https://www.imdb.com/title/tt0050083/mediaviewer/rm1466922497/?ref_=tt_ov_i"
#     )

# with app.app_context():
#     db.session.add(new_movie)
#     db.session.commit()

#update image link
# with app.app_context():
#     movie_id = 2
#     movie_to_update = db.session.execute(db.select(Movie).where(Movie.id == movie_id)).scalar()
#     movie_to_update.img_url = "https://image.tmdb.org/t/p/original/ow3wq89wM8qd5X7hWKxiRfsFf9C.jpg"
#     db.session.commit()


@app.route("/")
def home():
    result = db.session.execute(db.select(Movie).order_by(Movie.title))
    all_movies = result.scalars()
    return render_template("index.html", movies=all_movies)


if __name__ == '__main__':
    app.run(debug=True)
