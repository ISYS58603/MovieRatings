from flask import Flask
from api.routes import register_routes

app = Flask(__name__)

# Register the routes from the routes.py file
register_routes(app)

# Entry point for your API
if __name__ == "__main__":
    app.run()
