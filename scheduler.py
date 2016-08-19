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


if __name__ == "__main__":


    schedule.every().monday.at("00:01").do(change_goal_status)

    while True:
        schedule.run_pending()

