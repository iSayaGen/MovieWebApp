from models import Movie, User, db


class DataManager:
    """Handle database operations for MovieWeb."""

    def create_user(self, name: str) -> User:
        """Create and persist a new user."""
        user = User(name=name)

        db.session.add(user)
        db.session.commit()

        return user

    def get_user(self, user_id: int) -> User | None:
        """Return a user by ID, or None if it does not exist."""
        return db.session.get(User, user_id)

    def get_users(self) -> list[User]:
        """Return all users."""
        return db.session.execute(
            db.select(User)
        ).scalars().all()

    def get_movies(self, user_id: int) -> list[Movie]:
        """Return all movies belonging to a user."""
        return db.session.execute(
            db.select(Movie)
            .where(Movie.user_id == user_id)
            .order_by(Movie.name)
        ).scalars().all()

    def add_movie(self, movie: Movie) -> Movie:
        """Persist a new movie."""
        db.session.add(movie)
        db.session.commit()

        return movie

    def update_movie(
        self,
        user_id: int,
        movie_id: int,
        new_title: str,
    ) -> bool:
        """Update a movie if it belongs to the specified user."""
        movie = db.session.execute(
            db.select(Movie).where(
                Movie.id == movie_id,
                Movie.user_id == user_id,
            )
        ).scalar_one_or_none()

        if movie is None:
            return False

        movie.name = new_title
        db.session.commit()

        return True

    def delete_movie(self, user_id: int, movie_id: int) -> bool:
        """Delete a movie if it belongs to the specified user."""
        movie = db.session.execute(
            db.select(Movie).where(
                Movie.id == movie_id,
                Movie.user_id == user_id,
            )
        ).scalar_one_or_none()

        if movie is None:
            return False

        db.session.delete(movie)
        db.session.commit()

        return True
