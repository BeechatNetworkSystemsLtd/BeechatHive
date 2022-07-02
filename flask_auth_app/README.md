



##Create database
from project import db, create_app, models
db.create_all(app=create_app()) # pass the create_app result so Flask-SQLAlchemy gets the configuration.

##Activate environment
source auth/bin/activate

#Install requirements
pip install flask flask-sqlalchemy flask-login

##Export 
export FLASK_APP=project
export FLASK_DEBUG=1

##Run app
flask run --host=0.0.0.0
