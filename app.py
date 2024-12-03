from flask import Flask, redirect, render_template, request, url_for

app = Flask(__name__)

# #home page route
@app.route("/")
def index():
    return render_template("index.html")


#login route
@app.route("/login", methods=['GET','POST'])
def login():   
    if request.method == 'POST':
        name = request.form.get("username")    
        return redirect(url_for('home', name=name))
    return render_template("login.html")

#Home page
@app.route("/home")
def home():
    name = request.args.get("name")
    return render_template("home.html", name=name)

#logout
@app.route("/logout")
def logout():
    return redirect(url_for('login'))
