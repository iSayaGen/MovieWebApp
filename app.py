from pathlib import Path

from flask import Flask

from data_manager import DataManager
from models import db


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
def home():
    return "Welcome to MovieWeb App!"


if __name__ == "__main__":
    with app.app_context():
        db.create_all()

    app.run()