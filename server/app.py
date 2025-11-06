from flask import Flask, request, jsonify
from flask_migrate import Migrate
import os

app=Flask(__name__)

#database configuration
app.config['SQLALCHEMY_DATABASE_URI']= os.environ.get('DATABASE_URL', 'sqlite:///camping.db') #db location (SQLite file)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False

#import models and initialize db
from models import db, Camper, Activity, Signup
db.init_app(app) #connect db to flask app
migrate=Migrate(app,db) #set up migration for db changes

#create all tables
with app.app_context():
    db.create_all()

#root route to confirm the API is running
@app.route('/')
def hello():
    return {'message': 'camping fun API'} #returns a JSON message

#GET all campers
@app.route('/campers', methods=['GET'])
def get_campers():
    campers=Camper.query.all() #query the db for all camper records
    return jsonify([camper.to_dict() for camper in campers]) #convert each camper to dict, then to JSON array

#POST- create new camper
@app.route('/campers', methods=['POST'])
def create_camper():
    try:
        data=request.get_json() #get JSON data from request
        camper=Camper(name=data['name'], age=data['age']) #create a new camper instance
        db.session.add(camper) #add to db session
        db.session.commit() #save changes to db
        return jsonify(camper.to_dict()),201 #return created camper with 201 status
    except ValueError as e: #handling validation errors
        return jsonify({'errors':[str(e)]}), 400 #return error message with 401 error
    except Exception as e: #handling any other errors
        return jsonify({'errors':['invalid data']}), 400 #returns a generic error

# GET specific camper by id
@app.route('/campers/<int:id>', methods=['GET'])
def get_camper(id):
    camper=Camper.query.get(id)#find camper by id
    if not camper:
        return jsonify({'error':'Camper not found'}), 404 #return 404 if not found
    return jsonify(camper.to_dict(include_signups=True))#return camper data with signups

#PATCH (updating the camper by id)
@app.route('/campers/<int:id>', methods=['PATCH'])
def update_camper(id):
    camper=Camper.query.get(id) #find camper by id
    if not camper:
        return jsonify({'error':'Camper not found'}), 404
    try:
        data=request.get_json() #get update data
        if 'name' in data:
            camper.name=data['name'] #update name if provided
        if 'age' in data:
            camper.age=data['age'] #update age if provided
        db.session.commit()#save changes
        return jsonify(camper.to_dict()), 202 #return updated camper with 202 status
    except ValueError as e: #handle validation errors
        return jsonify({'errors':[str(e)]}), 400

#get all activities
@app.route('/activities', methods=['GET'])
def get_activities():
    activities=Activity.query.all() #query db for all activity records
    return jsonify([activity.to_dict() for activity in activities]) #convert to JSON array

#DELETE activity by id
@app.route('/activities/<int:id>', methods=['DELETE'])
def delete_activity(id):
    activity=Activity.query.get(id)#find the activity by id
    if not activity:
        return jsonify({'error':'Activity not found'}), 404 #return 404 if not found
    db.session.delete(activity) #delete from db
    db.session.commit()#save the changes
    return '', 204 #return empty response with 204 status
    
#POST(creating a new signup)
@app.route('/signups',methods=['POST'])
def create_signup():
    try:
        data=request.get_json()#get signup data
        signup=Signup(
            camper_id=data['camper_id'],
            activity_id=data['activity_id'],
            time=data['time']
        )
        db.session.add(signup) #add to db session
        db.session.commit()#save changes
        return jsonify(signup.to_dict(include_relations=True)), 201 #return created signup with nested data
    except ValueError as e: #handle validation errors
        return jsonify({'errors':[str(e)]}), 400
    except Exception as e: #handle other errors
        return jsonify({'errors':['Invalid data']}), 400

if __name__=='__main__':
    app.run(debug=True,port=5555)
