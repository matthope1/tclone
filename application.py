import sqlite3 as lite
import os
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash
from helpers import apology, login_required
from flask import Flask

#from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
#app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///tclone.db'
Session(app)

# db = SQLAlchemy(app)

con = lite.connect('tclone.db')

with con:

    cur = con.cursor()

    username = "testUser"
    password = generate_password_hash("testPass")

    # cur.execute("INSERT INTO users (username, hash) values (?,?)", (username, password))
    # cur.execute("INSERT INTO users VALUES (?, ?)", username, password)

    t = (username, ) #needs to provide a touple of values for the query

    cur.execute("SELECT * FROM users WHERE username=?", t)

    print(cur.fetchone())
    # for row in username_query:
        # print(row)


    con.commit()
# con.close()

print("insert complete")

@app.route('/')
@login_required
def index():
    return render_template("index.html") 

@app.route('/login', methods=["GET", "POST"])
def login():

    #user reached login via post
    if request.method == "POST": 
        print("login POST todo:")
    #user reached login via get  
    else:
        print("login GET todo: ")

@app.route('/register', methods=["GET","POST"])
def register():

    #user reached this route with the post method  
    if request.method == "POST":
        
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")
        
        if not username:
            return apology("Must enter a username")

        #connect to database
        con = lite.connect('tclone.db')

        with con:
            cur = con.cursor()
            q = (username, )
            username_query = cur.execute("SELECT * from users WHERE username=?", q)
            #print(cur.fetchone())

            #if the query doesn't return 0 rows then the username is not available 
            if cur.fetchone() != None:
                return apology("Username taken")

        if not password:
            return apology("Must enter a password")
            
        if password != confirmation:
            return apology("Passwords must match")

        hashed_pass = generate_password_hash(password)
        cur.execute("INSERT INTO users (username, hash) values (?,?)", (username, hashed_pass))

        flash("Registration successful")      
        return render_template("login.html")

    #user reached this route with the get method
    else:
        return render_template("register.html")

def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)

# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)








