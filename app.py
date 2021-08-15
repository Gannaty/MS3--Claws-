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
            "username": request.form.get("username").lower(),
            "password": generate_password_hash(request.form.get("password"))
        }
        mongo.db.users.insert_one(register)

        # Putting new user into 'session' cookie
        session["user"] = request.form.get("username").lower()
        flash("Registration successful")
        return redirect(url_for("profile", username=session["user"]))

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        # Check to see if username exists in mdb
        existing_user = mongo.db.users.find_one(
            {"username": request.form.get("username").lower()})

        if existing_user:
            # Make sure hashed password matches user input in form
            if check_password_hash(
                    existing_user["password"], request.form.get("password")):
                # If password matches, log user into
                # session and show welcome flash
                session["user"] = request.form.get("username").lower()
                flash("Welcome, {}".format(request.form.get("username")))
                return redirect(url_for(
                    "profile", username=session["user"]))
            else:
                # Password doesn't match, incorrect, user gets warning flash
                flash("Incorrect Username and/or Password")
                return redirect(url_for("login"))
        else:
            # Username doesn't match, incorrect, user gets warning flash
            flash("Incorrect Username and/or Password")
            return redirect(url_for("login"))

    return render_template("/login.html")


@app.route("/profile/<username>", methods=["GET", "POST"])
def profile(username):
    # Username variable = grab session user's username from db
    username = mongo.db.users.find_one(
        {"username": session["user"]})["username"]
    return render_template("profile.html", username=username)


@app.route("/logout")
def logout():
    # remove user from session
    flash("You have been logged out")
    session.pop("user")
    return redirect(url_for("login"))


# ------- Add post -------

@app.route("/add_post", methods=["GET", "POST"])
def add_post():
    """
    Registered users can upload their favourite recipes.
    """

    # user variable for user image
    user = mongo.db.users.find_one(
        {"username": session["user"]})

    if request.method == "POST":
        post = {
            "title": request.form.get("title"),
            "post_caption": request.form.get("post_caption"),
            "image": request.form.get("image"),
            "poster": session["user"],
        }

        mongo.db.posts.insert_one(post)
        flash("Post shared!")
        return redirect(url_for(
            "profile", username=session["user"]))

    return render_template(
        "/add_post.html", user=user, title="post_caption")


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)
