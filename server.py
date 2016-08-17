from flask import Flask, render_template, request, flash, session, redirect
from flask_debugtoolbar import DebugToolbarExtension

from jinja2 import StrictUndefined

from model import connect_to_db, db, User, Goal, Completion, Categories

#app variable binding for argument in connect_to_db function in model
app = Flask(__name__)


#added for Flask sessions and debugtoolbar use
app.secret_key = "ABC"
#to raise an error in Jinja2 so it can't pass silently
app.jinja_env.undefined = StrictUndefined
#bypasses bug that results in server restart for each update to jinja template
app.jinja_env.auto_reload = True


@app.route('/')
def index():
    """Homepage"""

    #To account if the user has already signed in
    #redirect them to their users goals
    if "user_id" in session:
        return redirect("/user/%s" % session["user_id"])
    else:
        return render_template('homepage.html')


@app.route('/sign_up')
def sign_up():
    """Form for a new user to register"""

    return render_template('register_form.html')


@app.route('/register', methods=['POST'])
def register():
    """Submits user sign up data and reroutes to homepage"""

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

    return render_template('login_form.html')


@app.route('/login', methods=['POST'])
def login_process():
    """Process the login and redirect user to homepage"""

    email = request.form["email"]
    password = request.form["pass1"]

    #queries goal_tracker db to see if user exists, returns
    #'None' if user does not exist
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

    #queries goal_tracker db table 'goals' to see if
    #the user in the session has goals in table
    goal = Goal.query.filter_by(user_id=user_id).first()

    if goal is None:
        flash("You have no goals! Let's create some!")
        return render_template('create_goal.html')
    else:
        #store users attributes as an object
        user = User.query.filter_by(user_id=user_id).one()
        #store a list of users goals as objects in list
        goals = Goal.query.filter_by(user_id=user_id).all()

        return render_template('user_goals.html',
                               user=user,
                               goals=goals)


@app.route('/submit_goals', methods=['POST'])
def submit_goals():
    """Submit user's created goal and reroutes to user goal page"""

    user_id = session["user_id"]

    cat_name = request.form.getlist('goal_type')

    for name in cat_name:
        if Categories.query.filter(Categories.cat_name == name):
            pass
        else:
            category = Categories(cat_name=name)
            db.session.add(category)
            db.session.commit()

    description = request.form['goal_description']

    times_per_week = int(request.form['times_per_week'])

    goal = Goal(user_id=user_id, description=description,
                num_of_times=times_per_week)

    db.session.add(goal)
    db.session.commit()

    flash("Your goal was added!")

    return redirect("/user/%s" % user_id)


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