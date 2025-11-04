from flask import Flask, request, jsonify
from flask_migrate import Migrate
import os

app=Flask(__name__)

#database configuration
app.config['SQLALCHEMY_DATABASE_URI']= os.environ.get('DATABASE_URL', 'sqlite:///camping.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False

#import models and initialize db
from models import db, Camper, Activity, Signup
db.init_app(app)
migrate=Migrate(app,db)

#create all tables
with app.app_context():
    db.create_all()

@app.route('/')
def hello():
    return {'message': 'camping fun API'}

#get all campers
@app.route('/campers', methods=['GET'])
def get_campers():
    campers=Camper.query.all()
    return jsonify([camper.to_dict() for camper in campers])

#get all activities
@app.route('/activities', methods=['GET'])
def get_activities():
    activities=Activity.query.all()
    return jsonify([activity.to_dict() for activity in activities])

if __name__=='__main__':
    app.run(debug=True,port=5555)
