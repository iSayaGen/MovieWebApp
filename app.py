import os
from pathlib import Path

import requests
from dotenv import load_dotenv
from flask import Flask, abort, flash, redirect, render_template, request, url_for
from sqlalchemy.exc import SQLAlchemyError

from data_manager import DataManager
from models import Movie, db


# Load environment variables from .env.
BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env")

OMDB_API_KEY = os.getenv("OMDB_API_KEY")
OMDB_API_URL = "https://www.omdbapi.com/"


app = Flask(__name__)

# Flask uses this for session data and flash messages.
app.config["SECRET_KEY"] = os.getenv(
    "SECRET_KEY",
    "dev-secret-key-change-me",
)

# Database configuration.
data_dir = BASE_DIR / "data"
data_dir.mkdir(exist_ok=True)

app.config["SQLALCHEMY_DATABASE_URI"] = (
    f"sqlite:///{data_dir / 'movies.db'}"
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Connect SQLAlchemy to Flask.
db.init_app(app)

# Create DataManager.
data_manager = DataManager()


@app.route("/")
def index():
    """Display all users."""
    users = data_manager.get_users()
    return render_template("index.html", users=users)


@app.route("/users", methods=["POST"])
def create_user():
    """Create a new user and return to the user list."""
    name = request.form.get("name", "").strip()

    if not name:
        flash("Please enter a name.", "error")
        return redirect(url_for("index"))

    try:
        data_manager.create_user(name)
    except SQLAlchemyError:
        flash("We couldn't create the user. Please try again.", "error")
        return redirect(url_for("index"))

    flash(f"User '{name}' was created successfully.", "success")
    return redirect(url_for("index"))


@app.route("/users/<int:user_id>/movies", methods=["GET"])
def get_movies(user_id):
    """Display all movies belonging to a user."""
    user = data_manager.get_user(user_id)

    if user is None:
        abort(404)

    movies = data_manager.get_movies(user_id)

    return render_template(
        "movies.html",
        movies=movies,
        user=user,
        user_id=user_id,
    )


@app.route("/users/<int:user_id>/movies", methods=["POST"])
def add_movie(user_id):
    """Look up a movie with OMDb and add it to the user's collection."""
    user = data_manager.get_user(user_id)

    if user is None:
        abort(404)

    title = request.form.get("title", "").strip()

    if not title:
        flash("Please enter a movie title.", "error")
        return redirect(url_for("get_movies", user_id=user_id))

    if not OMDB_API_KEY:
        app.logger.error("OMDB_API_KEY is not configured.")
        flash(
            "The movie service is not configured. "
            "Please try again later.",
            "error",
        )
        return redirect(url_for("get_movies", user_id=user_id))

    try:
        response = requests.get(
            OMDB_API_URL,
            params={
                "apikey": OMDB_API_KEY,
                "t": title,
            },
            timeout=10,
        )
        response.raise_for_status()
        data = response.json()

    except requests.RequestException:
        app.logger.exception("OMDb request failed for title '%s'.", title)
        flash(
            "We couldn't reach the movie service. "
            "Please try again later.",
            "error",
        )
        return redirect(url_for("get_movies", user_id=user_id))

    except ValueError:
        app.logger.exception("OMDb returned invalid JSON.")
        flash(
            "The movie service returned an invalid response.",
            "error",
        )
        return redirect(url_for("get_movies", user_id=user_id))

    if data.get("Response") != "True":
        error_message = data.get(
            "Error",
            "The movie could not be found.",
        )
        flash(error_message, "error")
        return redirect(url_for("get_movies", user_id=user_id))

    movie_title = data.get("Title")

    if not movie_title:
        app.logger.error("OMDb response did not contain a movie title.")
        flash(
            "The movie service returned incomplete information.",
            "error",
        )
        return redirect(url_for("get_movies", user_id=user_id))

    year_text = data.get("Year", "")
    try:
        year = int(year_text[:4])
    except (TypeError, ValueError):
        year = 0

    movie = Movie(
        name=movie_title,
        director=data.get("Director", "Unknown"),
        year=year,
        poster_url=data.get("Poster", ""),
        user_id=user_id,
    )

    try:
        data_manager.add_movie(movie)
    except SQLAlchemyError:
        flash(
            "We couldn't save the movie. Please try again.",
            "error",
        )
        return redirect(url_for("get_movies", user_id=user_id))

    flash(f"'{movie.name}' was added to your movies.", "success")
    return redirect(url_for("get_movies", user_id=user_id))


@app.route(
    "/users/<int:user_id>/movies/<int:movie_id>/update",
    methods=["POST"],
)
def update_movie(user_id, movie_id):
    """Update the title of a movie belonging to the current user."""
    new_title = request.form.get("title", "").strip()

    if not new_title:
        flash("Please enter a movie title.", "error")
        return redirect(url_for("get_movies", user_id=user_id))

    try:
        updated = data_manager.update_movie(
            user_id,
            movie_id,
            new_title,
        )
    except SQLAlchemyError:
        flash(
            "We couldn't update the movie. Please try again.",
            "error",
        )
        return redirect(url_for("get_movies", user_id=user_id))

    if not updated:
        abort(404)

    flash("Movie updated successfully.", "success")
    return redirect(url_for("get_movies", user_id=user_id))


@app.route(
    "/users/<int:user_id>/movies/<int:movie_id>/delete",
    methods=["POST"],
)
def delete_movie(user_id, movie_id):
    """Delete a movie belonging to the current user."""
    try:
        deleted = data_manager.delete_movie(user_id, movie_id)
    except SQLAlchemyError:
        flash(
            "We couldn't delete the movie. Please try again.",
            "error",
        )
        return redirect(url_for("get_movies", user_id=user_id))

    if not deleted:
        abort(404)

    flash("Movie deleted successfully.", "success")
    return redirect(url_for("get_movies", user_id=user_id))


@app.errorhandler(404)
def page_not_found(error):
    """Render the custom 404 page."""
    return render_template("404.html"), 404


@app.errorhandler(500)
def internal_server_error(error):
    """Render the custom 500 page."""
    db.session.rollback()
    return render_template("500.html"), 500


if __name__ == "__main__":
    with app.app_context():
        db.create_all()

    app.run()
