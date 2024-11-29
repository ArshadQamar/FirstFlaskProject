from flask import Flask, render_template, request

app = Flask(__name__)

# #home page route
@app.route("/")
def index():
    return render_template("index.html")


#login route
@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method=='POST':
       return "400" 

    return render_template("login.html")
