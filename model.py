"""Models and database functions for Hackbright Project: goal_tracker"""

from flask_sqlalchemy import SQLAlchemy

from model_util import *

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
    #This was added to account for eventual addition of user
    #data of timezone.
    time_zone = db.Column(db.String(25), nullable=True)

    def __repr__(self):

        return "<user_id=%s email=%s first=%s last=%s>" % (self.user_id,
                                                           self.email,
                                                           self.first,
                                                           self.last)


class Goal(db.Model):
    """Goal model for individual user"""

    __tablename__ = "goals"

    goal_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    description = db.Column(db.Text, nullable=False)
    num_of_times = db.Column(db.Integer, nullable=False)
    date_started = db.Column(db.DateTime(timezone=True),
                             nullable=False, default=make_timestamp)
    active = db.Column(db.Boolean, nullable=False, default=True)
    #UTC timezone date/time stamp.
    exempt = db.Column(db.Boolean, nullable=False, default=False)
    time_period = db.Column(db.Integer, default=7)
    #time_period unit is in DAYS.

    user = db.relationship('User', backref='goals')

    def __repr__(self):

        return "<goal_id=%s description=%s num_of_times=%s time_period=%s>" % (
            self.goal_id, self.description, self.num_of_times, self.time_period)


class Completion(db.Model):
    """Completion Model"""

    __tablename__ = "completions"

    comp_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    goal_id = db.Column(db.Integer, db.ForeignKey('goals.goal_id'))
    date_complete = db.Column(db.DateTime(timezone=True),
                              nullable=True, default=make_timestamp)
    #UTC timezone date/time stamp.
    reflection = db.Column(db.Text, nullable=True)

    goal = db.relationship('Goal', backref='completions')
    user = db.relationship('User', secondary='goals', backref='completions')

    def __repr__(self):

        return "<comp_id=%s date_complete=%s" % (self.comp_id, self.date_complete)


class Categories(db.Model):
    """Categories Model"""

    __tablename__ = "categories"

    #MANY TO MANY ASSOCIATION TABLE TO DO, SECONDARY RELATIONSHIP

    cat_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    cat_name = db.Column(db.String(50), nullable=False)

    goals = db.relationship('Goal', secondary='goal_cats', backref='categories')

    def __repr__(self):

        return "<cat_id=%s cat_name=%s>" % (self.cat_id, self.cat_name)


class GoalCat(db.Model):
    """Association Model to connect Goals and Categories"""

    __tablename__ = "goal_cats"

    goal_cat_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    goal_id = db.Column(db.Integer, db.ForeignKey('goals.goal_id'))
    cat_id = db.Column(db.Integer, db.ForeignKey('categories.cat_id'))

############################################################################

def init_app():
    from flask import Flask
    from server import app

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
    from server import app

#FIXME!! Need to add to db.create_all() if it doesn't exist already

    connect_to_db(app)
    print "Connected to DB."