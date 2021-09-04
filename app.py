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


# ------- Display all users posts -------

@app.route("/")
@app.route("/get_posts")
def get_posts():

    # Display posts newest first
    posts = list(mongo.db.posts.find().sort("_id", -1))

    return render_template("index.html", posts=posts)


# ------- Search for posts -------

@app.route("/search", methods=["GET", "POST"])
def search():
    query = request.form.get("query")
    posts = list(mongo.db.posts.find({"$text": {"$search": query}}))

    return render_template("index.html", posts=posts)


# ------- Register user -------

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


# ------- Login -------

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


# ------- Logout ----------------

@app.route("/logout")
def logout():
    # remove user from session
    flash("You have been logged out")
    session.pop("user")
    return redirect(url_for("login"))


# ------- Profile page with all current user posts ---------------

@app.route("/profile/<username>", methods=["GET", "POST"])
def profile(username):
    """
     Username variable = grab session user's username from db
    """
    username = mongo.db.users.find_one(
        {"username": session["user"]})["username"]

    # Add profile info from users collection
    user = mongo.db.users.find_one(
        {"username": session["user"]})

    if session["user"] == username:

        posts = list(
            mongo.db.posts.find({"poster": username.lower()}))

    # Find the post of user currently in session and display on profile page
    return render_template(
        "/profile.html", posts=posts, username=username, user=user)


# ------- Add/Edit profile info -------

@app.route("/edit_profile/<username>", methods=["GET", "POST"])
def edit_profile(username):
    """
    Registered users can upload profile pictures
    """

    username = mongo.db.users.find_one(
        {"username": session["user"]})["username"]

    # To look through and display user info
    user = mongo.db.users.find_one(
        {"username": session["user"]})

    if session["user"] == username:

        # Update profile function
        if request.method == "POST":

            mongo.db.users.update_one({'username': session['user']},
                                      {'$set': {
                                          'profile_img': request.form.get(
                                              'profile_img'),
                                          'profile_bio': request.form.get(
                                              'profile_bio')
                                      }})

            flash("{}'s Profile Updated!".format(
                    session["user"]))
            return redirect(url_for("profile", username=session["user"]))

    return render_template("/edit_profile.html", user=user, username=username)


# ------- Delete user profile -------

@app.route("/delete_user/<username>")
def delete_user(username):
    """
    Allows user to delete profile
    """

    if session["user"] == username:

        # Deletes user posts 
        mongo.db.posts.remove(
            {"poster": username.lower()})

        # Deletes user account 
        mongo.db.users.remove(
            {"username": username.lower()})
        flash("Profile Deleted")
        session.pop("user")

        return redirect(url_for("register"))

    else:
        # if wrong user
        flash("You do not have permission to do that!")
        return redirect(url_for("profile",
                                username=session["user"]))

# ------- Add post -------

@app.route("/add_post", methods=["GET", "POST"])
def add_post():
    """
    Registered users can upload posts about nail art
    """

    # Find if this user is the session user
    user = mongo.db.users.find_one(
        {"username": session["user"]})

    # Make the posts found a list to be interated over in
    # index.html to display all posts on the home page
    posts = list(mongo.db.posts.find())

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
        "/add_post.html", user=user, title="title", posts=posts)


# ------- Show each post on own page -------

@app.route("/posts.html/<post_id>")
def posts(post_id):

    post = mongo.db.posts.find_one(
        {"_id": ObjectId(post_id)})

    return render_template("/posts.html", post=post)


# ------- Edit post -------

@app.route("/edit_post.html/<post_id>", methods=["GET", "POST"])
def edit_post(post_id):

    if request.method == "POST":

        update_post = {
            "title": request.form.get("title"),
            "post_caption": request.form.get("post_caption"),
            "image": request.form.get("image"),
            "poster": session["user"]
        }

        mongo.db.posts.update(
            {"_id": ObjectId(post_id)}, update_post)

        flash("Post Updated!")
        return redirect(url_for(
            "profile", username=session["user"]))

    post = mongo.db.posts.find_one(
        {"_id": ObjectId(post_id)})

    return render_template("/edit_post.html", post=post)


# ------- Delete post -------

@app.route("/delete_post/<post_id>")
def delete_post(post_id):

    # Find post with ObjectId = to post_id variable
    mongo.db.posts.remove({"_id": ObjectId(post_id)})
    flash("Post deleted")

    # Redirect to session user profile page
    return redirect(url_for(
            "profile", username=session["user"]))


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)
