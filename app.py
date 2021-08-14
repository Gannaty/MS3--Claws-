import os

# Import flask, pymongo and BSON object ID
from flask import (
    Flask, flash, render_template,
    redirect, request, session, url_for)
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash

# Importing env only if the os can find the existing file path
if os.path.exists("env.py"):
    import env as config


# Creating an instance of Flask
app = Flask(__name__)

app.config["MONGO_DBNAME"] = os.environ.get("MONGO_DBNAME")
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
app.secret_key = os.environ.get("SECRET_KEY")


mongo = PyMongo(app)


@app.route("/")
@app.route("/get_posts")
def get_posts():
    posts = mongo.db.posts.find()
    return render_template("posts.html", posts=posts)

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        # Check if username inputted in the form matches any username
        # in mdb 'users' collection
        # If it matches, the user is exisitng. We store usernames in
        # .lower() for ease of comparison
        existing_user = mongo.db.users.find_one(
            {"username": request.form.get("username").lower()})

        if existing_user:
            flash("Username already exists")
            return redirect(url_for("register"))

        register = {
            "username" : request.form.get("username").lower(),
            "password" : generate_password_hash(request.form.get("password"))
        }
        mongo.db.users.insert(register)

        # Putting new user into 'session' cookie
        session["user"] = request.form.get("username").lower()
        flash("Registration successful")
        return render_template("register.html")


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)
