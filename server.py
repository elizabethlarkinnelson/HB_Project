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


    return render_template('homepage.html')


@app.route('/sign_up')
def sign_up():
    """The form fields for a new user to register"""

    return render_template('register_form.html')


@app.route('/register', methods=['POST'])
def register():
    """Submits user data input and reroutes to homepage"""

    email = request.form["email"]
    first_name = request.form["first_name"]
    last_name = request.form["last_name"]
    password = request.form["pass1"]

    new_user = User(email=email, first=first_name, last=last_name, password=password)

    db.session.add(new_user)
    db.session.commit()


    flash("Registered! %s, log in to set your goals!" % first_name) 
    return redirect('/')

@app.route('/login', methods=['GET'])
def login_form():
    """Display login form"""


    return render_template("login_form.html")

@app.route('/login', methods=['POST'])
def login_process():
    """Process the login and redirect user to homepage"""

    email = request.form["email"]
    password = request.form["pass1"]


    user = User.query.filter_by(email=email).first()

    if not user:
        flash("No such user")
        return redirect('/login')

    if user.password != password:
        flash("Incorrect password")
        return redirect('/login')

    session["user_id"] = user.user_id

    flash("Logged in")
    return redirect("/user/%s" % user.user_id)


@app.route('/user/<int:user_id>')
def user_goals(user_id):
    """Display user's goals"""

    user_id = session["user_id"]

    if Goal.query.filter(Goal.goal_id == None):
        flash("This week is full of possibility! Tell me what you can accomplish this week!")
        return render_template('create_goal.html')
        

    else:
        return render_template('user_goals.html')


#FIXME!!!!!!!!!


@app.route('/logout')
def logout():
    """Logs users out of the session"""

    del session["user_id"]
    flash("Logged Out.")
    return redirect('/')


if __name__ == "__main__":

    app.debug = True
    connect_to_db(app)
    DebugToolbarExtension(app)
    app.run(host="0.0.0.0")