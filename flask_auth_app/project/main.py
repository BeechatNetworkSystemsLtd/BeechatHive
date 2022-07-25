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
    subprocess.Popen(["""cd "/home/beechat/e-Paper-master/RaspberryPi_JetsonNano/python3/examples"
python3 epd_2in13_V2_test.py"""])
    return redirect(url_for('main.profile'))

@main.route('/startradio', methods=['POST'])
def startRadio():
    process = subprocess.Popen(['/bin/python3 /home/beechat/BeechatHive-main/flask_auth_app/project/receiver.py'], shell=True)
    #print(process.pid())
#    import time
#    print("Killing processin 10 seconds...")
#    time.sleep(10)
#    process = subprocess.Popen(['sudo kill ' + process.pid()], shell=True)
#   /bin/sudo /bin/python3
    #out, err = process.communicate()
    #print(out)
    #s = out.decode()
    
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