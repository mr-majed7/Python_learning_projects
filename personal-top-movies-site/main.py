from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
import requests
import os
import dotenv

dotenv.load_dotenv()


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


class RateMovieForm(FlaskForm):
    rating = StringField("Your Rating Out of 10 e.g. 9")
    review = StringField("Your Review")
    submit = SubmitField("Done")

class FIndMovieForm(FlaskForm):
    title = StringField("Movie Title", validators=[DataRequired()])
    submit = SubmitField("Add Movie")

@app.route("/")
def home():
    result = db.session.execute(db.select(Movie).order_by(Movie.ranking))
    all_movies = result.scalars().all()
    for i in range(len(all_movies)):
        all_movies[i].ranking = len(all_movies) - i
    db.session.commit()

    return render_template("index.html", movies=all_movies)

@app.route("/edit", methods=["GET", "POST"])
def rate_movie():
    form = RateMovieForm()
    movie_id = request.args.get("id")
    movie = db.get_or_404(Movie, movie_id)
    if form.validate_on_submit():
        movie.rating = float(form.rating.data)
        movie.review = form.review.data
        db.session.commit()
        return redirect(url_for('home'))
    return render_template("edit.html", movie=movie, form=form)

@app.route("/delete")
def delete():
    movie_id = request.args.get('id')
    movie_to_delete = db.get_or_404(Movie, movie_id)
    db.session.delete(movie_to_delete)
    db.session.commit()
    return redirect(url_for("home"))

@app.route("/add", methods=["GET", "POST"])
def add_movie():
    form = FIndMovieForm()
    if form.validate_on_submit():
        title = form.title.data
        url = "https://api.themoviedb.org/3/search/movie?"
        headers = {
            "accept": "application/json",
            "Authorization": os.getenv("API_READ_ACCESS_TOKEN")
        }
        response = requests.get(url=url, headers=headers, params={"query": title})
        data = response.json()["results"]
        print(data)
        return render_template('select.html', options=data)

    return render_template('add.html',form=form)


@app.route("/select")
def select():
    movie_id = request.args.get('id')
    if movie_id:
        url = f"https://api.themoviedb.org/3/movie/{movie_id}"
        headers = {
            "accept": "application/json",
            "Authorization": os.getenv("API_READ_ACCESS_TOKEN")
        }
        response = requests.get(url=url, headers=headers)
        data = response.json()
        new_movie = Movie(
            title=data["title"],
            year=data["release_date"].split("-")[0],
            description=data["overview"],
            img_url=f"https://image.tmdb.org/t/p/original/{data['poster_path']}"

        )
        db.session.add(new_movie)
        db.session.commit()
        return redirect(url_for('rate_movie', id=new_movie.id))



if __name__ == '__main__':
    app.run(debug=True)
