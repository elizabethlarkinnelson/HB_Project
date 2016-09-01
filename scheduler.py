import schedule
from model import *
from flask import Flask

app = Flask(__name__)
connect_to_db(app)


def change_goal_status():
    active_non_exempt_goals = Goal.query.filter((Goal.active == True) & (Goal.exempt == False)).all()
    for goal in active_non_exempt_goals:
        goal.active = False
        db.session.commit()

#A function that at 00:05 will take any goal that are
#inactive, but exempt and create another entry of that exact goal
#for the next week.  The previous instance of that goal
#will then be made unexempt.

def repeat_goal_inactivate_old_goal():
    repeat_goals = Goal.query.filter((Goal.active == False) & (Goal.exempt == True)).all()
    for goal in repeat_goals:
        user_id = goal.user_id
        description = goal.description
        num_of_times = goal.num_of_times
        new_goal = Goal(user_id=user_id, description=description,
                        num_of_times=num_of_times)
        db.session.add(new_goal)
        db.session.commit()

#FIX ME!!! 
#Need to add goal schedule for when "inactivating" that current
#weeks goals.
#Also, need to give server access to repeat_goal_inactivate_old_goal()
#so user can click to add the goal.


if __name__ == "__main__":


    schedule.every().monday.at("00:01").do(change_goal_status)


    while True:
        schedule.run_pending()
        

