import os
from pathlib import Path

import requests
from dotenv import load_dotenv
from flask import Flask, render_template, request, redirect, url_for

from data_manager import DataManager
from models import db, Movie


load_dotenv()

OMDB_API_KEY = os.getenv("OMDB_API_KEY")


app = Flask(__name__)

# Database configuration
basedir = Path(__file__).resolve().parent
data_dir = basedir / "data"
data_dir.mkdir(exist_ok=True)

app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{data_dir / 'movies.db'}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Connect SQLAlchemy to Flask
db.init_app(app)

# Create DataManager
data_manager = DataManager()


@app.route("/")
def index():
    users = data_manager.get_users()
    return render_template("index.html", users=users)


@app.route("/users", methods=["POST"])
def create_user():
    name = request.form["name"]
    data_manager.create_user(name)
    return redirect(url_for("index"))


@app.route("/users/<int:user_id>/movies", methods=["GET"])
def get_movies(user_id):
    movies = data_manager.get_movies(user_id)
    return render_template(
        "movies.html",
        movies=movies,
        user_id=user_id
    )


@app.route("/users/<int:user_id>/movies", methods=["POST"])
def add_movie(user_id):
    title = request.form["title"]

    response = requests.get(
        "https://www.omdbapi.com/",
        params={
            "apikey": OMDB_API_KEY,
            "t": title,
        },
        timeout=10,
    )

    data = response.json()

    if data.get("Response") == "False":
        return f"Movie not found: {data.get('Error', 'Unknown error')}", 404

    year_text = data.get("Year", "")

    try:
        year = int(year_text[:4])
    except (ValueError, TypeError):
        year = 0

    movie = Movie(
        name=data["Title"],
        director=data.get("Director", "Unknown"),
        year=year,
        poster_url=data.get("Poster", ""),
        user_id=user_id,
    )

    data_manager.add_movie(movie)

    return redirect(url_for("get_movies", user_id=user_id))


@app.route("/users/<int:user_id>/movies/<int:movie_id>/update", methods=["POST"])
def update_movie(user_id, movie_id):
    new_title = request.form["title"]

    data_manager.update_movie(movie_id, new_title)

    return redirect(url_for("get_movies", user_id=user_id))


@app.route("/users/<int:user_id>/movies/<int:movie_id>/delete", methods=["POST"])
def delete_movie(user_id, movie_id):
    data_manager.delete_movie(movie_id)

    return redirect(url_for("get_movies", user_id=user_id))


if __name__ == "__main__":
    with app.app_context():
        db.create_all()

    app.run()