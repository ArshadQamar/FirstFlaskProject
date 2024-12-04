from flask import Flask, redirect, render_template, request, url_for, session
from dotenv import load_dotenv
import os

# Load environment variables from the .env file
load_dotenv()

app = Flask(__name__)

# Set the secret key from the .env file
app.secret_key = os.getenv('SECRET_KEY')

# #home page route
@app.route("/")
def index():
    if 'username' in session:
        return f"you are logged in as {session['username']}. Go to <a href='{url_for('home')}'>Home</a>"
    return render_template("index.html")

# Login route
@app.route("/login", methods=['GET', 'POST'])
def login():   
    if request.method == 'POST':
        name = request.form.get("username")   # getting user name
        session['username'] = name
        return redirect(url_for('home'))
    
    if 'username' in session:
        return redirect(url_for('home'))
    
    return render_template("login.html")

# Home page
@app.route("/home")
def home():
    name = session.get("username")
    if not name:
        return redirect(url_for("login"))     
    return render_template("home.html", name=name)

# Logout
@app.route("/logout")
def logout():
    session.pop("username", None)  # Remove username from session
    return redirect(url_for('login'))
