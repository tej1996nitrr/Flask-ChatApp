import flask 
from flask import Flask, render_template,redirect,url_for
from  wtforms_fields import *
from models import *
from passlib.hash import pbkdf2_sha512
from flask_login import LoginManager,login_user,current_user,login_required,logout_user

app = Flask(__name__)
app.secret_key  = "secret"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=True
app.config['SQLALCHEMY_DATABASE_URI'] = "postgres://hjijzyacnjtvjb:e74232e2ab8db0c4509da69dd803e55a2a57eb41a6f0c9131a3b4cf2e3757b44@ec2-52-202-185-87.compute-1.amazonaws.com:5432/d47rf5bjth4ct6"
db = SQLAlchemy(app)

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
    if current_user.is_authenticated:
            return "Please login first."
    return "Chat with me"
@app.route("/logout",methods = ["GET"])
def logout():
    logout_user()
    return "Logged out using flask-login"

if __name__=="__main__":
    app.run(debug=True)
    
