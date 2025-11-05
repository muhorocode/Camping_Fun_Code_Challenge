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

#create new camper
@app.route('/campers', methods=['POST'])
def create_camper():
    try:
        data=request.get_json()
        camper=Camper(name=data['name'], age=data['age'])
        db.session.add(camper)
        db.session.commit()
        return jsonify(camper.to_dict()),201
    except ValueError as e:
        return jsonify({'errors':[str(e)]}), 400
    except Exception as e:
        return jsonify({'errors':['invalid data']}), 400


#get all activities
@app.route('/activities', methods=['GET'])
def get_activities():
    activities=Activity.query.all()
    return jsonify([activity.to_dict() for activity in activities])

if __name__=='__main__':
    app.run(debug=True,port=5555)
