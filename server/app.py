from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os

app=Flask(__name__)

#database configuration
app.config['SQLALCHEMY_DATABASE_URI']= os.environ.get('DATABASE_URL', 'sqlite:///camping.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False

db=SQLAlchemy(app)
migrate=Migrate(app,db)

@app.route('/')
def hello():
    return {'message': 'camping fun API is running'}

if __name__=='__main__':
    app.run(debug=True,port=5555)
