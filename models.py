from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column


db = SQLAlchemy()


class User(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)


class Movie(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    director: Mapped[str] = mapped_column(nullable=False)
    year: Mapped[int] = mapped_column(nullable=False)
    poster_url: Mapped[str] = mapped_column(nullable=False)
    imdb_id: Mapped[str] = mapped_column(nullable=False)

    user_id: Mapped[int] = mapped_column(
        ForeignKey("user.id"),
        nullable=False,
    )
