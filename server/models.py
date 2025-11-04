# Import database instance
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates

# Create db instance that will be initialized later
db = SQLAlchemy()

#camper model for the person attending camp
class Camper(db.Model):
    __tablename__='campers'
    
    # basic camper info
    id=db.Column(db.Integer, primary_key=True)
    name=db.Column(db.String, nullable=False)
    age=db.Column(db.Integer, nullable=False)
    
    #making sure name is not empty
    @validates('name')
    def validate_name(self,key,name):
        if not name or not name.strip():
            raise ValueError("Name is required")
        return name
    
    #making sure the age is between 8 and 18
    @validates('age')
    def validate_age(self,key,age):
        if not isinstance(age,int) or age <8 or age >18:
            raise ValueError("Age must be an integer between 8 and 18")
        return age

    #convert camper to dictionary for JSON response

    def to_dict(self):
        return{
            'id':self.id,
            'name':self.name,
            'age':self.age
        }
#activity model for camp activities
class Activity(db.Model):
    __tablename__='activities'

    #activity details
    id=db.Column(db.Integer, primary_key=True)
    name=db.Column(db.String, nullable=False)
    difficulty=db.Column(db.Integer, nullable=False)

    #convert activity to dictionary
    def to_dict(self):
        return{
            'id':self.id,
            'name':self.name,
            'difficulty':self.difficulty
        }

#signup model links campers to activities
class Signup(db.Model):
    __tablename__='signups'

    #signup information
    id=db.Column(db.Integer, primary_key=True)
    camper_id=db.Column(db.Integer, db.ForeignKey('campers.id'), nullable=False)
    activity_id=db.Column(db.Integer, db.ForeignKey('activities.id'), nullable=False)
    time=db.Column(db.Integer, nullable=False) # hour of the day between 0-23

    #making sure time is valid hour

    @validates('time')
    def validate_time(self,key,time):
        if not isinstance(time,int) or time <0 or time >23:
            raise ValueError("Time must be an integer between 0 and 23")
        return time

    #convert signup to dictionary
    def to_dict(self):
        return{
            'id':self.id,
            'camper_id':self.camper_id,
            'activity_id':self.activity_id,
            'time':self.time
        }