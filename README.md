# Camping Fun Code Challenge - Flask API

A Flask REST API for managing campers, activities, and signups for Access Camp.

## Technologies Used

- Flask, Flask-SQLAlchemy, Flask-Migrate
- SQLite Database
- Python 3.13

## Setup Instructions

```bash
# Clone and setup
git clone https://github.com/muhorocode/Camping_Fun_Code_Challenge.git
cd Camping_Fun_Code_Challenge

# Virtual environment
python3 -m venv env
source env/bin/activate

# Install and run
pip install -r requirements.txt
cd server
python app.py
```

API runs at `http://localhost:5555`

##  API Endpoints

### Campers
- `GET /campers` - List all campers
- `GET /campers/<id>` - Get camper with signups
- `POST /campers` - Create new camper
- `PATCH /campers/<id>` - Update camper

### Activities
- `GET /activities` - List all activities
- `DELETE /activities/<id>` - Delete activity

### Signups
- `POST /signups` - Create new signup

## Example Usage

```bash
# Create camper
curl -X POST http://localhost:5555/campers \
  -H "Content-Type: application/json" \
  -d '{"name": "Alice Johnson", "age": 12}'

# Get all campers
curl http://localhost:5555/campers
```

## Features

- Model validations (name required, age 8-18, time 0-23)
- Many-to-many relationships through signups
- Cascade deletes and proper error handling
- MVC architecture with SQLAlchemy ORM