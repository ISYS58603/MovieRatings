from flask import jsonify, request, Flask
from services import get_all_users, get_user_by_id, get_users_by_name, create_user, update_user, delete_user
from models import User, create_user_from_dict

# Sample data

app =   Flask(__name__)

@app.route('/users', methods=['GET'])
def get_users():
    return (jsonify(get_all_users()), 200)

@app.route('/users', methods=['POST'])
def add_new_user():
    new_user_dict = request.get_json()
    new_user = User(new_user_dict['id'], new_user_dict['user_name'], new_user_dict['email'])
    create_user(new_user)
    return jsonify({'message': 'User added', 'user': new_user}), 201

@app.route('/users/<int:user_id>', methods=['GET'])
def lookup_user_by_id(user_id):
    user = get_user_by_id(user_id)
    if user:
        return jsonify(user), 200
    return jsonify({'message': 'User not found'}), 404
