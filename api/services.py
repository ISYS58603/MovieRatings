import sqlite3
from models import User, Rating, Movie
from typing import List

# Set up a connection to the SQLite database
def get_db_connection():
    connection = sqlite3.connect('data/movie_data.db')
    connection.row_factory = sqlite3.Row  # This allows you to access columns by name
    return connection

# This is a conversion function that takes a list of rows from the database and converts them into a list of User objects
def convert_rows_to_user_list(users):
    all_users = []
    for user in users:
        user = User(user['user_id'], user['username'], user['email'])
        all_users.append(user)
    return all_users

def convert_rows_to_rating_list(ratings):
    all_ratings = []
    for rating in ratings:
        rating = Rating(rating['rating_id'], rating['user_id'], rating['movie_id'], rating['rating'], rating['review'], rating['date'])
        all_ratings.append(rating)
    return all_ratings

def convert_rows_to_movie_list(movies):
    all_movies = []
    for movie in movies:
        movie = Movie(movie['movie_id'], movie['title'], movie['genre'], movie['release_year'], movie['director'])
        all_movies.append(movie)
    return all_movies

def get_all_users() -> List[User]:
    # We need to start by getting the connection to the database
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Query the database for all users
    query = "SELECT user_id,username,email  FROM users"
    cursor.execute(query)
    
    users = cursor.fetchall()
    conn.close()
    
    # Convert this list of users into a list of User objects
    return convert_rows_to_user_list(users)

# This function will return a specific user based on the user_id or user_name
def get_user_by_id(user_id: int) -> User:
    # We need to start by getting the connection to the database
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Query the database for all users
    query = "SELECT user_id,username,email FROM users WHERE user_id = ?"
    # We need to pass the user_id as a tuple to be the parameters of the query
    cursor.execute(query, (user_id,))
    
    users = cursor.fetchall()
    conn.close()
    
    # Convert this list of users into a list of User objects, but only take the first object
    return convert_rows_to_user_list(users)[0]

# This function will return a list of users based on the user_name
# The starts_with parameter is used to determine if the user_name should start with the provided string
#   or if it should contain the provided string
def get_users_by_name(user_name: str, starts_with: bool =True) -> List[User]:
    # We need to start by getting the connection to the database
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Query the database for all users
    query = "SELECT user_id,username,email FROM users WHERE username like ?"
    
    # We use the % symbol as a wildcard to match any characters before or after the user_name
    params = f'{user_name}%' if starts_with else f'%{user_name}%'
    cursor.execute(query, (params,))
    
    users = cursor.fetchall()
    conn.close()
    
    # Convert this list of users into a list of User objects
    return convert_rows_to_user_list(users)

# Add a user to the database
def create_user(user: User):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    query = "INSERT INTO users (username, email) VALUES (?, ?)"
    cursor.execute(query, (user.user_name, user.email))
    
    conn.commit()
    conn.close()

# Update a user in the database
def update_user(user: User):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    query = "UPDATE users SET username = ?, email = ? WHERE user_id = ?"
    cursor.execute(query, (user.user_name, user.email, user.id))
    
    conn.commit()
    conn.close()

# Delete a user from the database
def delete_user(user_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    query = "DELETE FROM users WHERE user_id = ?"
    cursor.execute(query, (user_id,))
    
    conn.commit()
    conn.close()

if __name__ == '__main__':
        
    # Usage
    ## Test to see if all users are returned
    # print("Get all users")
    # all_users = get_all_users()
    # for user in all_users:
    #    print(user)

    ## Test to get a single user by id
    # print(get_user_by_id(1))

    ## Test to get a list of users by name
    # Test to get a list of users by name that start with the provided string
    # print('Starts with')
    # print("-----------")
    # for n in get_users_by_name('l'):
    #     print(n)

    # # Test to get a list of users by name that start with the provided string
    # print('Contains')
    # print("-----------")
    # for name in get_users_by_name('luke', False):
    #     print(name)

    # Test to create a user
    print("Create a user")
    print("-----------")
    new_user = User(None, 'test_user', 'testuser@example.com')
    create_user(new_user)
    added_user = get_users_by_name('test_user')[0]
    print(added_user)

    # Test to update a user
    print("Update a user")
    print("-----------")
    # Start by getting the user to update
    user_to_update = get_users_by_name('test_user')[0]
    print(user_to_update)
    # Update the user
    user_to_update.user_name = 'updated_user'
    update_user(user_to_update)
    # Get the user again to see the changes
    updated_user = get_user_by_id(user_to_update.id)
    print(updated_user)

    # # Test to remove a user 
    # print('Now delete the user')
    # print("-----------")
    # # Start by getting the last user put into the database
    # last_user = get_all_users()[-1]
    # delete_user(last_user.id)
    # print(get_users_by_name(last_user.user_name))