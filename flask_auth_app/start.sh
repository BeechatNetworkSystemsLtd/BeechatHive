##Activate environment
source /home/beechat/flask_auth_app/auth/bin/activate

##Create database
#python -c 'from project import db, create_app, models'
#python -c 'db.create_all(app=create_app())' # pass the create_app result so Flask-SQLAlchemy gets the configuration.
#echo 'Created database'

#Install requirements
#pip install flask flask-sqlalchemy flask-login

##Export 

export FLASK_APP=project
export FLASK_DEBUG=1
echo 'EXPORTed variables'


#make self-signed SSL cert
#openssl req -x509 -newkey rsa:4096 -nodes -out cert.pem -keyout key.pem -days 365

##Run app
flask run --host=0.0.0.0 --cert=/home/beechat/flask_auth_app/cert.pem --key=/home/beechat/flask_auth_app/key.pem


