import os

# Import flask
from flask import Flask

# Importing env only if the os can find the existing file path
if os.path.exists("env.py"):
    import env


# Creating an instance of Flask
app = Flask(__name__)


@app.route("/")
def hello():
    return "hello World...again!"


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)
