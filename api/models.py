

# In this file, we define the classes that represent the data in our application.
# If our classes got to be too numerous, we could refactor them into separate files, 
#  likely if we went this path, we would put them into a models directory.
class User:
    
    def __init__(self, id: int, user_name: str, email: str):
        self.id = id
        self.user_name = user_name
        self.email = email
        self.date_joined = None

    def __repr__(self):
        return f'<User {self.id} - {self.user_name}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_name': self.user_name,
            'email': self.email,
            'date_joined': self.date_joined
        }

# This function will take a dictionary and return a User object    
def create_user_from_dict( data: dict) -> User:
        return User(data['id'], data['user_name'], data['email'])
    
class Rating:
        
    def __init__(self, rating_id: int, user_id: int, movie_id: int, rating: int, review: str, date: str):
        self.rating_id = rating_id
        self.user_id = user_id
        self.movie_id = movie_id
        self.rating = rating
        self.review = review
        self.date = date
        
    def __repr__(self):
        return f'<Rating {self.rating_id}>'
    
    def to_dict(self):
        return {
            'rating_id': self.rating_id,
            'user_id': self.user_id,
            'movie_id': self.movie_id,
            'rating': self.rating,
            'review': self.review,
            'date': self.date
        }

# This function will take a dictionary and return a Rating object
def create_rating_from_dict(data: dict) -> Rating:
    return Rating(data['rating_id'], data['user_id'], data['movie_id'], data['rating'], data['review'], data['date'])    

class Movie:
    
    def __init__(self, movie_id: int, title: str, genre: str, release_year: int, director: str):
        self.movie_id = movie_id
        self.title = title
        self.genre = genre
        self.release_year = release_year
        self.director = director
        
    def __repr__(self):
        return f'<Movie {self.movie_id} - {self.title}>'
    
    def to_dict(self):
        return {
            'movie_id': self.movie_id,
            'title': self.title,
            'genre': self.genre,
            'release_year': self.release_year,
            'director': self.director
        }

# This function will take a dictionary and return a Movie object
def create_movie_from_dict(data: dict) -> Movie:
    return Movie(data['movie_id'], data['title'], data['genre'], data['release_year'], data['director'])