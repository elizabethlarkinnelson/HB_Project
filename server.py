from flask import Flask, render_template, request, flash, session, redirect, jsonify
from flask_debugtoolbar import DebugToolbarExtension

from datetime import datetime
import pytz

from jinja2 import StrictUndefined

from model import connect_to_db, db, User, Goal, Completion, Categories, Reminders


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

    #If the user is already signed in, redirect to goals page
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

    #Check if email already in db
    if User.query_by_email(email) is True:
        flash("Email already registered!")
        return redirect('/sign_up')

    #If email not already in db, create user in db
    else:
        User.create_user(email, first_name, last_name, password)

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

    if User.query_by_email(email) is False:
        flash("No such user")
        return redirect('/login')

    if (User.user_info_object(email)).password != password:
        flash("Incorrect password")
        return redirect('/login')

    session["user_id"] = (User.user_info_object(email)).user_id

    flash("Logged in")
    return redirect("/user/%s" % session["user_id"])


@app.route('/user/<int:user_id>')
def user_goals(user_id):
    """Display user's goals"""

    user_id = session["user_id"]

    if Goal.query_by_user_id(user_id) is False:
        flash("You have no goals! Let's create some!")
        return render_template('create_goal.html')
    else:

        user = User.query_by_user_id(user_id)

        goals = Goal.query_by_user_id(user_id)

        #FIXME!! When refactoring code, need to add % completion
        #which is already written, but needs to be added
        #as a class method.  This needs to passed through
        #so when the modal appears for text reminders
        #goals which have already been completed for the week
        #don't show up!

        goals_counts = {}

        for goal in goals:
            goal_count = Completion.query.filter_by(goal_id=goal.goal_id).count()
            goals_counts[goal.goal_id] = goal_count

        pacific = pytz.timezone('US/Pacific')
        now = datetime.now(tz=pacific)
        week_day = now.strftime("%A")

        return render_template('user_goals.html',
                               week_day=week_day,
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

    times_complete = 0
    times_total = 0

    #FIX ME!! Need to complete count of all completions for a specific goal
    for goal in goals:
        completions = Completion.query.filter((Goal.goal_id == goal.goal_id)
                                              & (Completion.goal_id == goal.goal_id)).count()
        times_complete += completions
        times_total += goal.num_of_times

    percentage_complete = int((float(times_complete) / float(times_total)) * 100)

    return jsonify(percentage_complete=percentage_complete)

#FIXME!!!
#Need route to deal with goal reminders


@app.route('/update_reminders.json', methods=['POST'])
def set_text_reminder():
    """Create new reminder id in database"""

    goal_id = request.form.get("goal_id")

    week_day = request.form.get("week_day")

    reminder = Reminders(goal_id=goal_id, text_days=week_day)
    db.session.add(reminder)
    db.session.commit()

    return jsonify(week_day=week_day, goal_id=goal_id)


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

    