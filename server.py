from flask import Flask, render_template, request, flash, session, redirect, jsonify
from flask_debugtoolbar import DebugToolbarExtension

from datetime import datetime


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

    #FIX ME!!! NEED TO WRITE CODE TO ACCOUNT FOR USER EMAIL ALREADY
    #EXISTING

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

        goals_counts = {}

        for goal in goals:
            goal_count = Completion.query.filter_by(goal_id=goal.goal_id).count()
            goals_counts[goal.goal_id] = goal_count

        return render_template('user_goals.html',
                               user=user,
                               goals=goals,
                               goals_counts=goals_counts)


@app.route('/add_goal')
def add_goal():
    """Allow's user to add goals."""

    return render_template('create_goal.html')


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


@app.route("/update_completions.json", methods=['POST'])
def get_completion_info():
    """Get the info for goal completion"""

    goal_id = request.form.get("goal_id")
    completion = Completion(goal_id=int(goal_id))
    db.session.add(completion)
    db.session.commit()

    goal = Goal.query.filter(Goal.goal_id == int(goal_id)).one()

    completions = goal.completions

    total_completions = 0

    for completion in completions:
        total_completions += 1

    if (float(total_completions) / float(goal.num_of_times)) != 1:
        num_left = (goal.num_of_times - total_completions)
        if num_left == 1:
            message = "Just " + str(num_left) + " time left!"
            remove_button = False
            return jsonify(message=message,
                           remove_button=remove_button, goal_id=goal_id)

        else:
            message = "Just " + str(num_left) + " times left!"
            remove_button = False
            return jsonify(message=message,
                           remove_button=remove_button, goal_id=goal_id)

    else:
        message = "You've completed " + goal.description + " for the week!"
        remove_button = True
        return jsonify(message=message,
                       remove_button=remove_button, goal_id=goal_id)

    return jsonify("Hi")


@app.route('/goal_visualization')
def goal_vis():
    """Displays a page where user can input parameters to visualize
    previous goals"""

    return render_template('goal_visualization.html')


@app.route('/goal_completion_data.json', methods=['GET'])
def goal_completion_data():
    """Query the database for user's goal/completion info"""

    user_id = session["user_id"]

    #Returns an object with all user info.  Currently not using!
    user = User.query.filter(User.user_id == user_id).one()

    #This will return a list of objects of user's goals
    goals = user.goals

    print"\n\n\n\n\n\n", goals, "\n\n\n\n\n\n"
    completions = user.completions

    #Working on creating a dictionary to pass through
    #in JSON
    goals_info = []
    #Iterate through a list of goal objects
    #adding the goal class attributes to a dictionary
    #that is appended to a list and eventually sent
    #to success handler in JSON in file data_vis.js
    for goal in goals:
        for completion in completions:
            if goal.goal_id == completion.goal_id:
                one_goal_info = {}

                one_goal_info["comp_id"] = completion.comp_id

                one_goal_info["goal_id"] = goal.goal_id
                one_goal_info["description"] = goal.description
                one_goal_info["num_of_times"] = goal.num_of_times

                #For date started I am converting the date to a list
                #2016-08-24 would be [2016, 08, 24]
                time = goal.date_started.strftime("%A, %B, %d, %Y")
                one_goal_info["date_started"] = time

                one_goal_info["active"] = goal.active
                one_goal_info["exempt"] = goal.exempt
                one_goal_info["time_period"] = goal.time_period

                #FIX ME!!!!!
                goals_info.append(one_goal_info)

    return jsonify(goals_info=goals_info)


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

    