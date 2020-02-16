from flask import Flask
app = Flask(__name__)
app.secret_key = "key"

@app.route("/",methods = ['GET','POST'])
def index():
    return "I am alive"

if __name__=="__main__":
    app.run(debug=True)
