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

@main.route('/startradio', methods=['POST'])
def startRadio():
    subprocess.Popen(['/bin/python3 /home/beechat/BeechatHive-main/flask_auth_app/project/receiver.py'], shell=True)
    return redirect(url_for('main.profile'))

@main.route('/killradio', methods=['POST'])
def killRadio():
    subprocess.Popen(["sh /home/beechat/BeechatHive-main/flask_auth_app/project/killradio.sh"], shell=True)
    return redirect(url_for('main.profile'))


@main.route('/sendmessage', methods =["GET", "POST"])
def gfg():
    if request.method == "POST":
       # getting input with name = fname in HTML form
       gateway = request.form.get("gateway")

       # getting input with name = lname in HTML form
       xmppaddress = request.form.get("xmppaddress")

       message = request.form.get("message")
       print("/bin/python3 /home/beechat/BeechatHive-main/flask_auth_app/project/sender.py \"<G>"+gateway+"</G><T>"+ xmppaddress +"</T><M>"+ message+"</M>\"")

       subprocess.Popen(["/bin/python3 /home/beechat/BeechatHive-main/flask_auth_app/project/sender.py \"<G>"+gateway+"</G><T>"+ xmppaddress +"</T><M>"+ message+"</M>\"" ], shell=True)
       
       #print(process.args())
    return redirect(url_for('main.profile'))

    
@main.route('/getmessages', methods=['POST']) 
@login_required
def content(): 
    with open('messages.txt', 'r') as f: 
        text=f.read()
        print(text)
        return render_template('profile.html', messages=text, name=current_user.name) 
        