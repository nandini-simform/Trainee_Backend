from json import dumps
from bson import ObjectId
from flask import Flask, request, jsonify
from pymongo import MongoClient
from flask_cors import CORS
from flask_jwt_extended import JWTManager, create_access_token, jwt_required
from werkzeug.security import check_password_hash

import os
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env

app = Flask(__name__)
CORS(app)

# Setup MongoDB Client
#app.config["MONGO_URI"] = "mongodb://localhost:27017/your_db_name"  # Replace with your actual DB
  # Choose a secret key

client = MongoClient(os.getenv('MONGO_URI'))
db = client['mydatabase']  # Replace with your database name if different
collection = db['users']

app.config["JWT_SECRET_KEY"] = "admin123"  # Get secret key from .env
jwt = JWTManager(app)

# Register new user (with hashed password)
@app.route('/api/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    # Check if username already exists
    existing_user = db.users.find_one({"username": username})
    if existing_user:
        return jsonify({"message": "Username already taken"}), 400

    # Hash the password before storing
    hashed_password = generate_password_hash(password)

    # Store the user in the database
    db.users.insert_one({'username': username, 'password': hashed_password})

    return jsonify({'message': 'User registered successfully'}), 201

# Login user and generate JWT token
@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    # Check if the user exists in the database
    user = db.users.find_one({"username": username})

    if user and check_password_hash(user['password'], password):
        # Generate JWT token for the user
        access_token = create_access_token(identity=username)
        return jsonify({'message': 'Login successful', 'access_token': access_token}), 200
    else:
        return jsonify({'message': 'Invalid username or password'}), 401
    
# Get all documents (GET endpoint) - Example, not login related.
@app.route('/get', methods=['GET'])
def get_documents():
    data = list(collection.find()) 
    print(data)
    for docs in data:
        docs['_id'] = str(docs['_id'])
     # Exclude the MongoDB _id field
    return jsonify(data), 200
 
# Create a new document (POST endpoint) - Example, not login related.
@app.route('/post', methods=['POST'])
def post_document():
    data = request.get_json()  # Get data from the request body
    if not data:
        return jsonify({"error": "No data provided"}), 400
    collection.insert_one(data)
    return jsonify({"message": "Data added"}), 201

# Update an existing document (PUT endpoint) - Example, not login related.
# @app.route('/put/<string:id>', methods=['PUT'])
# def update_document(id):
#     data = request.get_json()
#     if not data:
#         return jsonify({"error": "No data provided"}), 400
#     result = collection.update_one({"_id": id}, {"$set": data})
#     if result.matched_count > 0:
#         return jsonify({"message": "Document updated"}), 200
#     else:
#         return jsonify({"error": "Document not found"}), 404
@app.route('/delete/<id>', methods=['DELETE'])
def delete_document(id):
    try:
        result = db.users.delete_one({"_id": ObjectId(id)})
        if result.deleted_count > 0:
            return jsonify({"message": "Document deleted"}), 200
        else:
            return jsonify({"error": "Document not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500
if __name__ == '__main__':
    #to run docker container
    app.run(host='0.0.0.0', port=(os.getenv('port')), debug=True)
# for running locally
    # app.run(host='0.0.0.0', port=5000, debug=True)