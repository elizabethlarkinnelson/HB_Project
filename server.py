from flask import Flask, render_template, request, flash, session, redirect
from flask_debugtoolbar import DebugToolbarExtension

from jinja2 import StrictUndefined

from model import connect_to_db, db, User, Goal, Completion, Categories

# #App declaration for connect_to_db function in model
app = Flask(__name__)


# #This is added so Flask sessions and the debugtoolbar can be used
app.secret_key = "ABC"
# #To raise an error in Jinja2 so it pass silently
app.jinja_env.undefined = StrictUndefined


@app.route('/')
def index():
    """Homepage."""

    return render_template("homepage.html")


if __name__ == "__main__":

    app.debug = True
    connect_to_db(app)
    DebugToolbarExtension(app)
    app.run(host="0.0.0.0", port=5000)