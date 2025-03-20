# Trainee Backend

This is the backend of the full-stack application built with **Flask**. The backend interacts with a **MongoDB** database and exposes **GET**, **POST**, and **PUT** endpoints to interact with the data.

## Features

- **GET**: Fetches all records from the MongoDB database.
- **POST**: Creates new records in the MongoDB database.
- **PUT**: Updates existing records in the MongoDB database.

## Prerequisites

- **Python** (latest version)
- **MongoDB** or **MongoDB Atlas**
- **pip** (Python package manager)

## Getting Started

###  Clone the repository

1.Clone the backend repository to your local machine:

```bash
git clone https://github.com/yourusername/trainee_backend.git
cd trainee_backend

2. Set up a virtual environment
python -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate

3. Install dependencies
  pip install -r requirements.txt

4. Set up environment variables
 MONGO_URI=mongodb://your_mongodb_connection_uri

5. Start the Flask server
python app.py
