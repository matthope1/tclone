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

    # print(cur.fetchone())
    # for row in username_query:
        # print(row)


    con.commit()
con.close()

# print("app starting...")

@app.route('/', methods=["GET","POST"])
@login_required
def index():
    if request.method == "POST":
        tweet = request.form.get("tweet")

        if not tweet:
            return apology("Must provide text for tweet")
        
        uid = session["user_id"] 
        make_post(uid,tweet)

        flash("tweeted")
        return redirect("/")
        
    else:
        tweet_list = []
        con = lite.connect("tclone.db")        
        with con:

            cur = con.cursor()

            tweet_query = cur.execute("SELECT username, post, like_count FROM users JOIN tweets")

            for row in tweet_query:
                list = []
                list.append(row[0])
                list.append(" ".join(row[1].split("\r\n")))

                list.append(row[2])

                # print(row)
                # print(row[0])
                # print(row[1])
                # print(row[2])
                print(list)
                tweet_list.append(list)
            con.commit()
        con.close()

        return render_template("index.html", tweets = tweet_list) 

@app.route('/logout')
def logout():

    session.clear()

    flash("logout sucessful!")
    return redirect("/")

@app.route('/login', methods=["GET", "POST"])
def login():
    
    session.clear()
    #user reached login via post
    if request.method == "POST": 

        username = request.form.get("username")
        password = request.form.get("password")

        if not username:
            return apology("Must provide a username")

        if not password:
            return apology("Must provide a password")

        #print("username: ", username)
        #print("password: ", password)


        id = None
        #connect to database
        con = lite.connect('tclone.db')

        with con:
            cur = con.cursor()

            username_touple = (username, )
            query = cur.execute("SELECT username, hash, id from users WHERE username=?", username_touple)

            queryData = cur.fetchone()

            if not queryData:
                return apology("invalid username/password")

            hash = queryData[1]
            userId = queryData[2]

            if not check_password_hash(hash, password):
                return apology("invalid password")
            
        con.close()

        session["user_id"] = userId
        return redirect("/")

    #user reached login via get  
    else:
        print("reached login via get")

        return render_template("login.html")

@app.route('/register', methods=["GET","POST"])
def register():
    #user reached this route with the post method  
    if request.method == "POST":
        
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")
        
        if not username:
            return apology("Must provide a username")

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
        
        # print("Username: ", username)
        # print("hashedPass: ", hashed_pass)

        cur.execute("INSERT INTO users (username, hash) values (?,?)", (username, hashed_pass))

        con.commit()
        con.close()

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


# helper functions for database interaction  
def make_post(uid, tweet):
    #To do
    con = lite.connect('tclone.db')
        #To do 
    with con:
        cur = con.cursor() 
        data_touple = (uid, tweet) 
        cur.execute("INSERT INTO tweets (uid, post, date) VALUES (?, ?, CURRENT_TIMESTAMP)", data_touple)

        #queryData = cur.fetchone()
        con.commit()

    con.close()






