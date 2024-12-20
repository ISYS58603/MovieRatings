import pytest
from run import create_app
from api.models import User, Rating, Movie, create_user_from_dict
from api import services
from flask import json


@pytest.fixture(scope="module")
def test_client():
    # Set up Flask test client
    flask_app = create_app()
    flask_app.config["TESTING"] = True
    with flask_app.test_client() as testing_client:
        yield testing_client


@pytest.fixture(scope="function")
def test_user():
    # Create a known user for testing purposes
    user = User(None, "known_user", "knownuser@example.com")
    user.id = services.create_user(user)
    yield user
    # Delete the known user after the test
    services.delete_user(user.id)


@pytest.fixture(scope="function")
def test_movie():
    # Create a new movie for testing purposes
    movie = Movie(None, "test_movie", "test_genre", release_year=2024, director="Test Director")
    movie.movie_id = services.create_movie(movie)
    yield movie
    # Delete the movie after the test
    services.delete_movie(movie.movie_id)

@pytest.fixture(scope="function")
def known_rating(test_user, test_movie):
    # Create a new rating for testing purposes via API
    rating = Rating(
            rating_id=None,
            user_id=test_user.id,
            movie_id=test_movie.movie_id,
            rating=4.5,
            review="Great movie!",
            date="03/03/2024",
        )
    rating_id = services.create_rating(rating)
    rating.rating_id = rating_id
    
    yield rating
    
    # Delete the rating after the test
    services.delete_rating(rating_id)


@pytest.fixture(scope="function")
def test_ratings(test_user, test_movie):
    """Fixture to set up multiple ratings for a movie."""
    ratings = [
        Rating(rating_id=None, user_id=test_user.id, movie_id=test_movie.movie_id, rating=4.5, review="Great movie!", date="03/03/2024"),
        Rating(rating_id=None, user_id=test_user.id, movie_id=test_movie.movie_id, rating=3.0, review="Not bad!", date="04/30/2024"),
        Rating(rating_id=None, user_id=test_user.id, movie_id=test_movie.movie_id, rating=5.0, review="Excellent movie!", date="8/13/2024"),
    ]
    for rating in ratings:
        rating_id = services.create_rating(rating)
        rating.rating_id = rating_id

    yield ratings

    # Clean up after tests
    for rating in ratings:
        services.delete_rating(rating.rating_id)


class TestDatabaseConnection:
    def test_create_connection(self, test_client):
        response = test_client.get("/api/connection")
        assert response.status_code == 200

    def test_run_query(self, test_client):
        response = test_client.get("/api/users?username=%%")
        assert response.status_code == 200
        data = response.get_json()
        assert len(data) > 0


class TestUserRoutes:
    def test_get_all_users(self, test_client):
        response = test_client.get("/api/users")
        assert response.status_code == 200 , "Response code is not 200"
        data = response.get_json()
        assert len(data) > 0, "No users found"

    def test_get_user_by_id(self, test_client, test_user):
        response = test_client.get(f"/api/users/{test_user.id}")
        assert response.status_code == 200, "Response code is not 200"
        user = response.get_json()
        assert user is not None, "User not found"
        assert user["id"] == test_user.id, "User ID does not match"
        assert user["username"] == test_user.username, "Username does not match"

    def test_get_users_by_starts_with_name(self, test_client, test_user):
        partial_name = test_user.username[:3]
        response = test_client.get(f"/api/users?starts_with={partial_name}")
        assert response.status_code == 200, "Response code is not 200"
        users = response.get_json()
        assert len(users) > 0   , "No users found"
        for user in users:
            assert partial_name in user["username"].lower(), "Partial name not found in username"

        # Now test for the opposite case, where we shouldn't get the user back
        response = test_client.get("/api/users?starts_with=xxxy")
        assert response.status_code == 200, "Response code is not 200"
        users = response.get_json()
        assert len(users) == 0,    "User found with non-existent partial name"

    def test_get_users_by_contains_name(self, test_client, test_user):
        partial_name = test_user.username[3:]
        response = test_client.get(f"/api/users?contains={partial_name}")
        assert response.status_code == 200, "Response code is not 200"
        users = response.get_json()
        assert len(users) > 0 , "No users found"
        for user in users:
            assert partial_name in user["username"].lower() , "Partial name not found in username"

    def test_create_user(self, test_client):
        user_data = {"username": "test_user", "email": "testuser@example.com"}
        response = test_client.post("/api/users", json=user_data)
        assert response.status_code == 201, "Response code is not 201"
        data = response.get_json()
        user_id = data["user"]["id"]
        assert user_id is not None , "User ID is None"

        # Now get the user back and check that it is the same
        response = test_client.get(f"/api/users/{user_id}")
        user = response.get_json()
        assert user["username"] == user_data["username"], "Username does not match"
        assert user["email"] == user_data["email"] ,    "Email does not match"
        test_client.delete(f"/api/users/{user_id}")

    def test_update_user(self, test_client, test_user):
        # Update the user
        updated_data = {"username": "updated_user", "email": "knownuser@example.com"}
        response = test_client.put(f"/api/users/{test_user.id}", json=updated_data)
        assert response.status_code == 200, "Response code is not 200"

        # Verify update
        response = test_client.get(f"/api/users/{test_user.id}")
        updated_user = response.get_json()
        assert updated_user["username"] == "updated_user", "Username does not match"

    def test_delete_user(self, test_client, test_user):
        # Delete the user
        response = test_client.delete(f"/api/users/{test_user.id}")
        assert response.status_code == 200, "Response code is not 200"

        # Verify deletion
        response = test_client.get(f"/api/users/{test_user.id}")
        assert response.status_code == 404, "Response code is not 404"


class TestMovieRoutes:
    def test_get_all_movies(self, test_client):
        response = test_client.get("/api/movies")
        assert response.status_code == 200, "Response code is not 200"
        data = response.get_json()
        assert len(data) > 0, "No movies found"

    def test_get_movie_by_id(self, test_client,test_movie):
        response = test_client.get(f"/api/movies/{test_movie.movie_id}")
        assert response.status_code == 200, "Response code is not 200"
        movie = response.get_json()
        assert movie is not None, "Movie not found"
        assert movie["movie_id"] == test_movie.movie_id, "Movie ID does not match"
        assert movie["title"] == test_movie.title, "Title does not match"
        
    def test_create_movie(self, test_client):
        movie_data = {
            "title": "test_movie",
            "genre": "test_genre",
            "release_year": 2024,
            "director": "Test Director",
        }
        response = test_client.post("/api/movies", json=movie_data)
        assert response.status_code == 201, "Response code is not 201"
        data = response.get_json()
        movie_id = data["movie"]["movie_id"]
        assert movie_id is not None, "Movie ID is None"

        # Now get the movie back and check that it is the same
        response = test_client.get(f"/api/movies/{movie_id}")
        movie = response.get_json()
        assert movie["title"] == movie_data["title"], "Title does not match"
        assert movie["genre"] == movie_data["genre"], "Genre does not match"
        assert movie["release_year"] == movie_data["release_year"], "Release year does not match"
        assert movie["director"] == movie_data["director"], "Director does not match"
        test_client.delete(f"/api/movies/{movie_id}")

    def test_delete_movie(self, test_client, test_movie):
        # Delete the movie
        response = test_client.delete(f"/api/movies/{test_movie.movie_id}")
        assert response.status_code == 200, "Response code is not 200"

        # Verify deletion
        response = test_client.get(f"/api/movies/{test_movie.movie_id}")
        assert response.status_code == 404, "Response code is not 404"

    def test_update_movie(self, test_client, test_movie):
        # Update the movie
        updated_data = {
            "title": "updated_movie",
            "genre": "test_genre",
            "release_year": 2024,
            "director": "Test Director",
        }
        response = test_client.put(f"/api/movies/{test_movie.movie_id}", json=updated_data)
        assert response.status_code == 200, "Response code is not 200"

        # Verify update
        response = test_client.get(f"/api/movies/{test_movie.movie_id}")
        updated_movie = response.get_json()
        assert updated_movie["title"] == "updated_movie", "Title does not match"

class TestReviewRoutes:

    def test_create_review(self, test_client, test_movie, test_user):
        rating_data = {
            "user_id": test_user.id,
            "movie_id": test_movie.movie_id,
            "rating": 5,
            "review": "Great movie!",
            "date": "3/3/2024",
        }
        response = test_client.post("/api/ratings", json=rating_data)
        assert response.status_code == 201, "Response code is not 201"
        data = response.get_json()
        rating_id = data["rating"]["rating_id"]
        assert rating_id is not None, "Rating ID is None"

        # Now get the review back and check that it is the same
        response = test_client.get(f"/api/ratings/{rating_id}")
        rating = response.get_json()
        assert rating["rating"] == 5 , "Rating does not match"
        assert rating["review"] == "Great movie!", "Review does not match"
        test_client.delete(f"/api/ratings/{rating_id}")

    def test_get_review_by_id(self, test_client, known_rating):
        response = test_client.get(f"/api/ratings/{known_rating.rating_id}")
        assert response.status_code == 200, "Response code is not 200"
        rating = response.get_json()
        assert rating is not None , "Rating not found"
        assert rating["rating_id"] == known_rating.rating_id, "Rating ID does not match"
        assert rating["rating"] == known_rating.rating, "Rating does not match"


    def test_get_ratings_by_movie(self, test_client, test_movie, test_ratings):
        """Test getting ratings for a specific movie by its ID."""
        response = test_client.get(f"/api/movies/{test_movie.movie_id}/ratings")
        assert response.status_code == 200
        data = response.get_json()
        ratings = data.get("ratings", None)
        assert len(ratings) == len(test_ratings) , "Number of ratings does not match"

        for rating, rating_data in zip(test_ratings, ratings):
            assert rating_data["rating"] == rating.rating, "Rating does not match"
            assert rating_data["review"] == rating.review, "Review does not match"
