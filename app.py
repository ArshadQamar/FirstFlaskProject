from flask import Flask, redirect, render_template, request, url_for, session
from dotenv import load_dotenv
from app_db import initialize_db, initialize_message_table
import os, sqlite3

# Load environment variables from the .env file
load_dotenv()

# Check if the database file exists
if not os.path.exists("app.db"):
    print("Database file not found. Initializing database...")
    initialize_db()  # Call the function from app_db to create the database
    print("Database initialized successfully!")

# Check if the message table exists
initialize_message_table()

# Connecting to sqlite3
def get_db():
    connection = sqlite3.connect("app.db")
    connection.row_factory = sqlite3.Row
    return connection


#initializing flask app
app = Flask(__name__)

# Set the secret key from the .env file
app.secret_key = os.getenv('SECRET_KEY')

# home page route
@app.route("/")
def index():
    if 'username' in session:
        return f"you are logged in as {session['username']}. Go to <a href='{url_for('home')}'>Home</a>"
    return render_template("index.html")


# Login route
@app.route("/login", methods=['GET', 'POST'])
def login():   
    if request.method == 'POST':

        # connecting to database
        connection = get_db()
        cursor = connection.cursor()

        # getting user name and password
        name = request.form.get("username")
        password = request.form.get("password")  

        # authenticating the user
        try:
            
            #fetching user info
            cursor.execute("SELECT * FROM users WHERE username = ?",(name,))
            user = cursor.fetchone()

            if user:
                if user['password'] == password:
                    session['username'] = user['username']
                    return redirect(url_for('home'))
                
                return "Incorrect password"
            
            return "User does not exist"
        
        except Exception as e:
            return f"An error has occured {e}"

        finally:
            connection.close()

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

        #connecting to database
        connection = get_db()
        cursor = connection.cursor()

        #getting username , email and password
        username = request.form.get("username")
        password = request.form.get("password")
        email = request.form.get("email")

        try:

            #check if username exists
            cursor.execute("SELECT COUNT(*) FROM users WHERE username = ?", (username,))
            dup_username = cursor.fetchone()

            if dup_username[0] > 0:
                return "Username already exists"

            #check if email exists
            cursor.execute("SELECT COUNT(*) FROM users WHERE email= ?", (email,))
            dup_email = cursor.fetchone()

            if dup_email[0] > 0:
                return "Email already exists"
            
            #Inserting new user to the database
            cursor.execute("INSERT INTO users (username ,email, password) VALUES (?, ?, ?)",(username, email, password))
            
            # Commit the changes to the database
            connection.commit()

            return f"Signed up successfully, proceed to <a href='{url_for('login')}'>login</a>"
        
        except Exception as e:
            return f"an error occurred {e}"


        finally:
            # closing the connection
            connection.close()
        

    return render_template("signup.html")

@app.route('/profile', methods=['GET', 'POST'])
def profile():

    #getting the user id stored in session
    if 'username' not in session:
        return redirect(url_for('login'))

    username = session['username']
    try:
        #connecting to database
        connection = get_db()
        cursor = connection.cursor()
        # Query the database for user data based on the user_id
        cursor.execute("SELECT * FROM users where username = ?", (username,))
        user = cursor.fetchone()


        if request.method == 'POST':
            new_username = request.form.get("username")
            new_email = request.form.get("email")
            new_password = request.form.get("password")

            if new_username:
                cursor.execute("SELECT * FROM users WHERE username = ?",(new_username,))
                if cursor.fetchone():
                    return "Username already exists"
                cursor.execute("UPDATE users SET username = ? WHERE username = ?",(new_username, username))
                print(f"Updated username to {new_username}")
                session['username'] = new_username
                connection.commit()
                return "username updated successfully"

            if new_email:
                cursor.execute("SELECT * FROM users WHERE username = ?",(new_email,))
                if cursor.fetchone():
                    return "Username already exists"
                cursor.execute("UPDATE users SET email = ? WHERE email ' ?",(new_email, new_email))
                connection.commit()
                return "email updated successfully"

            if new_password:
                cursor.execute("UPDATE users SET password = ? WHERE username = ?",(new_password, username))
                connection.commit()
                return "password updated successfully"
           # If user data is found, return the user data
     
    except Exception as e:
        return f"An error occured {e}"

    finally:
        connection.close()

        # If user data is found, return the user data
    if user:
        return render_template("profile.html", user=user)
    else:
        return "User not found."

@app.route('/messages', methods = ['GET', 'POST'])
def messages():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        recipient = request.form.get('recipient')
        message = request.form.get('message')
        sender = session['username']

        try:
            connection = get_db()
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM users WHERE username = ?", (recipient,))
            if cursor.fetchone():
                cursor.execute("INSERT INTO messages (sender_username, receiver_username, message) VALUES (?, ?, ?)", (sender, recipient, message))
                connection.commit()
                return "Message sent successfully"
            return "Recipent not found"
        except Exception as e:
            return f"An error occured {e}"
        finally:
            connection.close()


    user = session['username']
    try:
        connection = get_db()
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM messages WHERE receiver_username = ?", (user,))
        messages = cursor.fetchall()

    except Exception as e:
        return f"An error occured {e}"
    finally:
        connection.close()
    
    return render_template("messages.html", messages=messages)
    
    
    
    

    

