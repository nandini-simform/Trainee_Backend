from flask import Flask, request, jsonify
from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env

app = Flask(__name__)

# Setup MongoDB Client
client = MongoClient(os.getenv('MONGO_URI'))
db = client['mydatabase']
collection = db['users']

# Get all documents (GET endpoint)
@app.route('/get', methods=['GET'])
def get_documents():
    data = list(collection.find({}, {'_id': 0}))  # Exclude the MongoDB _id field
    return jsonify(data), 200

# Create a new document (POST endpoint)
@app.route('/post', methods=['POST'])
def post_document():
    data = request.get_json()  # Get data from the request body
    if not data:
        return jsonify({"error": "No data provided"}), 400
    collection.insert_one(data)
    return jsonify({"message": "Document created"}), 201

# Update an existing document (PUT endpoint)
@app.route('/put/<string:id>', methods=['PUT'])
def update_document(id):
    data = request.get_json()
    if not data:
        return jsonify({"error": "No data provided"}), 400
    result = collection.update_one({"_id": id}, {"$set": data})
    if result.matched_count > 0:
        return jsonify({"message": "Document updated"}), 200
    else:
        return jsonify({"error": "Document not found"}), 404

if __name__ == '__main__':
    app.run(debug=True)
