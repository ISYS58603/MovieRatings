import unittest
import pytest
import api.services as services
from api.models import User, Rating, Movie  

class TestDB(unittest.TestCase):

    def setUp(self) -> None:
        return super().setUp()

    def test_create_connection(self):
        conn = services.get_db_connection()
        self.assertIsNotNone(conn)
        conn.close()

class TestUserDB(unittest.TestCase):

    def test_get_all_users(self):
        all_users = services.get_all_users()
        self.assertGreater(len(all_users), 0)

    def test_get_user_by_id(self):
        user = services.get_user_by_id(1)
        self.assertIsNotNone(user)
        self.assertEqual(user.id, 1)
        self.assertEqual(user.username, "jane_doe")

    def test_get_users_by_starts_with_name(self):
        users = services.get_users_by_name("jane")
        self.assertGreater(len(users), 0)
        for user in users:
            self.assertTrue("jane" in user.username.lower())
        # Now test for the opposite case, where we shouldn't get the user back
        users = services.get_users_by_name("wilson")
        self.assertEqual(len(users), 0)

    def test_get_users_by_contains_name(self):
        users = services.get_users_by_name("jane",starts_with=False)
        self.assertGreater(len(users), 0)
        for user in users:
            self.assertTrue("jane" in user.username.lower())
        # Now test for a user where just a part of the name is in the username
        users = services.get_users_by_name("wilson", starts_with=False)
        self.assertGreater(len(users), 0)
        for user in users:
            self.assertTrue("wilson" in user.username.lower())

    def setup_known_user(self) -> User:
        # Create a known user for testing purposes
        known_user = User(None, "known_user", "knownuser@example.com")
        known_user.id = services.create_user(known_user)
        return known_user

    def teardown_known_user(self, user_id):
        # Delete the known user after the test
        services.delete_user(user_id)

    def test_create_user(self):
        new_user = User(None, "test_user", "testuser@example.com")
        new_user.id = services.create_user(new_user)
        self.assertIsNotNone(new_user.id)
        # Now get the user back and check that it is the same
        user = services.get_user_by_id(new_user.id)
        self.assertEqual(user.username, new_user.username)
        self.assertEqual(user.email, new_user.email)
        services.delete_user(new_user.id)

    def test_update_user(self):
        # Create a new user
        known_user = self.setup_known_user()

        # Update the user
        known_user.username = "updated_user"
        services.update_user(known_user)
        updated_user = services.get_user_by_id(known_user.id)
        self.assertEqual(updated_user.username, "updated_user")

        # Delete the user
        self.teardown_known_user(known_user.id)
    
    def test_delete_user(self):
        # Create a new user
        known_user = self.setup_known_user()

        # Delete the user
        services.delete_user(known_user.id)
        deleted_user = services.get_user_by_id(known_user.id)
        self.assertIsNone(deleted_user)

# Add a test class for the Movie database operations
# This test class is a little more complex as we are going to use "fixtures"
#  Fixtures allow us to setup and teardown resources before and after tests
class TestMovieDB(unittest.TestCase):
    
    @pytest.fixture(scope="class")
    def movie_fixture(test_client):
        # Create a movie
        movie = Movie(None, "test_movie", "test_genre", release_year=2024, director="Test Director")
        movie.id = services.create_movie(movie)
        yield movie
        # Clean up
        services.delete_movie(movie.id)
        
    def test_get_all_movies(self):
        all_movies = services.get_all_movies()
        self.assertGreater(len(all_movies), 0)

    def test_create_movie(self):
        new_movie = Movie(None, "test_movie", "test_genre", release_year=2024, director="Test Director")
        new_movie.id = services.create_movie(new_movie)
        self.assertIsNotNone(new_movie.id)
        # Now get the movie back and check that it is the same
        movie = services.get_movie_by_id(new_movie.id)
        self.assertEqual(movie.title, new_movie.title)
        self.assertEqual(movie.genre, new_movie.genre)
        self.assertEqual(movie.release_year, new_movie.release_year)
        self.assertEqual(movie.director, new_movie.director)
        services.delete_movie(new_movie.id)

    def test_delete_movie(self):
        # Create a new movie
        new_movie = Movie(None, "test_movie", "test_genre", release_year=2024, director="Test Director")
        new_movie.id = services.create_movie(new_movie)

        # Delete the movie
        services.delete_movie(new_movie.id)
        deleted_movie = services.get_movie_by_id(new_movie.id)
        self.assertIsNone(deleted_movie)
    
    def test_update_movie(self, movie_fixture):
        # Update the movie
        movie_fixture.title = "updated_movie"
        services.update_movie(movie_fixture)
        updated_movie = services.get_movie_by_id(movie_fixture.id)
        self.assertEqual(updated_movie.title, "updated_movie")

    # def test_get_movie_by_id(self, movie_fixture):
    #     movie = services.get_movie_by_id(movie_fixture.id)
    #     self.assertIsNotNone(movie)
    #     self.assertEqual(movie.id, movie_fixture.id)
    #     self.assertEqual(movie.title, movie_fixture.title)
    
if __name__ == '__main__':
    unittest.main()
