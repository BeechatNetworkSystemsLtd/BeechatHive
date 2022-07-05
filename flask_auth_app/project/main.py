from flask import Blueprint, render_template, request, redirect, url_for
import subprocess
from flask_login import login_required, current_user
from . import db

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/profile')
@login_required
def profile():
    return render_template('profile.html', name=current_user.name)

@main.route('/startscreen', methods=['POST'])
def startScreen():
    subprocess.Popen(["""cd "/home/beechat/e-Paper/RaspberryPi_JetsonNano/python/examples"
python epd_2in13_V2_test.py"""])
    return redirect(url_for('main.profile'))

@main.route('/startradio', methods=['POST'])
def startRadio():
    process = subprocess.Popen(['sudo /bin/python /home/beechat/flask_auth_app/project/receiver.py'], shell=True)
#   /bin/sudo /bin/python
    #out, err = process.communicate()
    #print(out)
    #s = out.decode()
    
    return redirect(url_for('main.profile'))

@main.route('/killscreen', methods=['POST'])
def killScreen():
    # screenid=$(ps aux | grep epd | awk -F '${epd}' '{print $1}' | awk  '{print $2}' | awk '{print $1}' | sed -n 1p |cut -d " " -f1); kill $screenid
    # kill $screenid
    subprocess.Popen(["/home/beechat/flask_auth_app/killscreen.sh"])
    return redirect(url_for('main.profile'))


@main.route('/sendmessage', methods =["GET", "POST"])
def gfg():
    if request.method == "POST":
       # getting input with name = fname in HTML form
       gateway = request.form.get("gateway")

       # getting input with name = lname in HTML form
       xmppaddress = request.form.get("xmppaddress")

       message = request.form.get("message")
       print("sudo /bin/python /home/beechat/flask_auth_app/project/sender.py \"<G>"+gateway+"</G><T>"+ xmppaddress +"</T><M>"+ message+"</M>\"")

       subprocess.Popen(["sudo /bin/python /home/beechat/flask_auth_app/project/sender.py \"<G>"+gateway+"</G><T>"+ xmppaddress +"</T><M>"+ message+"</M>\"" ], shell=True)
       
       #print(process.args())
    return redirect(url_for('main.profile'))