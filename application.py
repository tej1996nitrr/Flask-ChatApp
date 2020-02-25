import flask 
from flask import Flask, render_template,redirect,url_for,flash
from  wtforms_fields import *
from models import *
from passlib.hash import pbkdf2_sha512
from flask_login import LoginManager,login_user,current_user,login_required,logout_user
from flask_socketio import SocketIO,send,emit,join_room,leave_room
from time import localtime,strftime
from datetime import datetime

app = Flask(__name__)
app.secret_key  = "secret"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=True
app.config['SQLALCHEMY_DATABASE_URI'] = "postgres://hjijzyacnjtvjb:e74232e2ab8db0c4509da69dd803e55a2a57eb41a6f0c9131a3b4cf2e3757b44@ec2-52-202-185-87.compute-1.amazonaws.com:5432/d47rf5bjth4ct6"
db = SQLAlchemy(app)
socketio = SocketIO(app)
ROOMS = [
    "lounge","news","games","coding"
]
login = LoginManager(app)
login.init_app(app)

@login.user_loader  
def load_user(id):
    return User.query.get(int(id))

@app.route("/", methods = ["GET","POST"])
def index():
    reg_form = RegistrationForm()
    if reg_form.validate_on_submit():
        username  =reg_form.username.data
        password = reg_form.password.data
        hashed_pwd = pbkdf2_sha512.hash(password)
        user = User(username=username,password=hashed_pwd)
        db.session.add(user)
        db.session.commit()
        flash("Registered Successfully. Please login.",category='success')
        return redirect(url_for('login'))
    return render_template("index.html",form=reg_form)


@app.route('/login',methods = ["GET","POST"])
def login():
    login_form = LoginForm()
    if login_form.validate_on_submit():
        user_object = User.query.filter_by(username = login_form.username.data).first()
        login_user(user_object)
        
        return redirect(url_for('chat'))
        
    return render_template("login.html",form = login_form)

@app.route("/chat",methods = ["GET","POST"])
# @login_required
def chat():
    # if not current_user.is_authenticated:
    #     flash("Please Login",category='danger')
    #     return redirect(url_for('login'))
        
    return render_template('chat.html',username=current_user.username,rooms=ROOMS)
   
@app.route("/logout",methods = ["GET"])
def logout():
    logout_user()
    flash("Logged out successfully","success")
    return redirect(url_for('login'))

@socketio.on('message') #name of the event-"message"
def message(data):
    print(f"\n\n{data}\n\n")
    send(
        {
            'msg':data['msg'],
            'username':data['username'],
            'time_stamp':strftime('%b-%d',localtime()),
            'room':data['room']
        }
    )
    # emit('some-event','this is a custom event message')
@socketio.on('join')
def join(data):
    join_room(data['room'])
    send({'msg':data['username'] + " has joined the room "+ data['room']},room = data['room'])

@socketio.on('leave')
def leave(data):
    join_room(data['room'])
    send({'msg':data['username'] + " has left the room "+ data['room']},room = data['room'])


if __name__=="__main__":
    socketio.run(app)
    # app.run(debug=True)
    
