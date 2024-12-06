from flask import Flask, redirect, render_template, request, url_for, session
from dotenv import load_dotenv
import os

# Load environment variables from the .env file
load_dotenv()

app = Flask(__name__)

# Set the secret key from the .env file
app.secret_key = os.getenv('SECRET_KEY')

#Initializing Database
db ={}

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
        # getting user name and password
        name = request.form.get("username")
        password = request.form.get("password")  

        if name in db:
            if db[name]["password"] == password:
                session['username'] = name
                return redirect(url_for('home'))
            return "incorrect password"
        return "user not found"

    if 'username' in session:
        #Output after GET request
        return redirect(url_for('home'))                            
    
    return render_template("login.html")

# Home page
@app.route("/home")
def home():

    # getting the username from the session started and storing it in name
    name = session.get("username")
                                                   
    
    if not name:
    # returning login page if there's no session
        return redirect(url_for("login"))                           
    
    # returning home.html by injecting name variable of home route to name variable present in html jinja template
    return render_template("home.html", name=name)                  

# Logout
@app.route("/logout")
def logout():
    # Remove username from session
    session.pop("username", None)                                    
    return redirect(url_for('login'))

# Sign up Form
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    
    if request.method == 'POST':
        username = request.form.get("username")
        password = request.form.get("password")
        email = request.form.get("email")
        

        #check for duplicate username
        if username in db:
            return "Username already exists, please choose a different one."
        
        #check for duplicate email
        for user in db.values():
            if user[email] == email:
                return "Email already exists, please try a different one."
        
        #store data of the user
        db[username]={"email": email, "password":password}
        print(db)
        return f"Signed up successfully, proceed to <a href='{url_for('login')}'>login</a>"
        

    return render_template("signup.html")