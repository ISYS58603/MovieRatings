import pandas as pd
from pathlib import Path
import sqlite3
    
# Set the path of where to find the data files
RAW_DATA_PATH = Path(__file__).parent / 'data'

# Set the path of where to save the SQLite database
DATABASE_PATH = Path(__file__).parents[1] / 'data'

# Load the data into the SQLite database
def load_data():
    # Read the data files into pandas dataframes
    movie_data = pd.read_csv(RAW_DATA_PATH / 'movies.csv', index_col=0)
    rating_data = pd.read_csv(RAW_DATA_PATH / 'ratings.csv', index_col=0)
    user_data = pd.read_csv(RAW_DATA_PATH / 'users.csv', index_col=0)
    
    # Create the tables in the SQLite database
    create_tables()
    
    # Create a SQLite database
    conn = sqlite3.connect(DATABASE_PATH / 'movie_data.db')
    # Write the dataframes to the database
    movie_data.to_sql('movies', conn, if_exists='append', index=False)
    rating_data.to_sql('ratings', conn, if_exists='append', index=False)
    user_data.to_sql('users', conn, if_exists='append', index=False)
    print('Data loaded into SQLite database')

def create_tables():
    # Create a SQLite database
    conn = sqlite3.connect(DATABASE_PATH / 'movie_data.db')
    cursor = conn.cursor()
    
    # Create the tables in the database
    cursor.execute('''DROP TABLE IF EXISTS movies ''')
    cursor.execute('''
                   CREATE TABLE IF NOT EXISTS movies (
                movie_id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT,
                genre TEXT,
                release_year INTEGER,
                director TEXT)
                ''')
    
    cursor.execute('''DROP TABLE IF EXISTS ratings''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS ratings (
            rating_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            movie_id INTEGER,
            rating INTEGER,
            review TEXT,
            date DATE
        )
    ''')
    
    cursor.execute('''DROP TABLE IF EXISTS users''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            email TEXT,
            date_joined DATE
        )
    ''')
    
    conn.commit()
    conn.close()
    
    print('Tables created in SQLite database')


def test_data_load():
    # Query the database to make sure the data was loaded
    conn = sqlite3.connect(DATABASE_PATH / 'movie_data.db')
    query = 'SELECT * FROM movies'
    movies = pd.read_sql(query, conn, index_col='movie_id')
    print(movies.head())

if __name__ == '__main__':
    load_data()
    test_data_load()
   