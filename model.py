"""Models and database functions for Hackbright Project: goal_tracker"""

from flask_sqlalchemy import SQLAlchemy
import datetime

db = SQLAlchemy()

##############################################################################

class User(db.Model):
    """User of goal_tracker website"""

    __tablename__ = "users"

    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    email = db.Column(db.String(50), unique=True, nullable=False)
    first = db.Column(db.String(25), nullable=False)
    last = db.Column(db.String(25), nullable=False)
    password = db.Column(db.String(25), nullable=False)

    
    def __repr__(self):

        return "<user_id=%s email=%s first=%s last=%s>" % (self.user_id,
            self.email, self.first, self.last)


class Goal(db.Model):
    """Goal model for individual user"""

    __tablename__ = "goals"

    goal_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    description = db.Column(db.Text, nullable=False)
    num_of_times = db.Column(db.Integer, nullable=False)
    time_period = db.Column(db.Integer, default=7)
    ##Time_period unit is in DAYS.

    users = db.relationship('User', backref='goals')

    def __repr__(self):

        return "<goal_id=%s description=%s num_of_times=%s time_period=%s>" % (
            self.goal_id, self.description, self.num_of_times, self.time_period)



class Completion(db.Model):
    """Completion Model"""

    __tablename__ = "completions"

    comp_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    goal_id = db.Column(db.Integer, db.ForeignKey('goals.goal_id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    date_complete = db.Column(db.DateTime(timezone=True), nullable=True)
    reflection = db.Column(db.Text, nullable=True)

    goals = db.relationship('Goal', backref='completions')
    users = db.relationship('User', backref='completions')


    def __repr__(self):

        return "<comp_id=%s date_complete=%s" % (self.comp_id, self.date_complete)


class Categories(db.Model):
    """Categories Model"""

    __tablename__ = "categories"

    cat_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    cat_name = db.Column(db.String(50), nullable=False)
    goal_id = db.Column(db.Integer, db.ForeignKey('goals.goal_id'))

    goals = db.relationship('Goal', backref='categories')


    def __repr__(self):

        return "<cat_id=%s cat_name=%s>" % (self.cat_id, self.cat_name)
    



def init_app():
    from flask import Flask
    app = Flask(__name__)

    connect_to_db(app)
    print "Connected to DB."


def connect_to_db(app):
    """Connect the database to our Flask app."""

    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres:///goal_tracker'
    app.config['SQLALCHEMY_ECHO'] = True
    db.app = app
    db.init_app(app)


if __name__ == "__main__":
    #To utilize database interactively
    from flask import Flask

    app = Flask(__name__)

    connect_to_db(app)
    print "Connected to DB."