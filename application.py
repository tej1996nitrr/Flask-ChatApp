import flask 
from flask import Flask, render_template,redirect,url_for
from  wtforms_fields import *
from models import *
from passlib.hash import pbkdf2_sha512

app = Flask(__name__)
app.secret_key  = "secret"
app.config['SQLALCHEMY_DATABASE_URI'] = "postgres://hjijzyacnjtvjb:e74232e2ab8db0c4509da69dd803e55a2a57eb41a6f0c9131a3b4cf2e3757b44@ec2-52-202-185-87.compute-1.amazonaws.com:5432/d47rf5bjth4ct6"
db = SQLAlchemy(app)

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
        return "Logged In "
    return render_template("login.html",form = login_form)

if __name__=="__main__":
    app.run(debug=True)
    
