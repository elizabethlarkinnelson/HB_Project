"""Models and db functions for goal_tracker db"""

from flask_sqlalchemy import SQLAlchemy


#Creating the session object where we can perform transactions.
db = SQLAlchemy()


#Composing Object Relation Models(ORM)

#Creating first table named "users"
class User(db.Model):

    """User model."""

    __tablename__ = "users"

    user_id = db.Column(db.Integer,
                        primary_key=True,
                        autoincrement=True,
                        db.ForeignKey('goals.user_id'))
                        #DOUBLE CHECK THIS RELATIONSHIP AFTER GOALS
                        #TABLE CREATED!
    email = db.Column(db.String(50),
                        unique=True
                        nullable=False)
    first = db.Column(db.String(25),
                        nullable=False)
    last = db.Column(db.String(25),
                        nullable=False)
    password = db.Column(db.String(25),
                        nullable=False)

    goals = db.relationship('Goal', backref="users")
    #DOUBLE CHECK THIS RELATIONSHIP AFTER GOALS TABLE CREATED!



#Creating second table name "goals"
class Goal(db.Model):

    """Goal model."""


    __tablename__ = "goals"


    goal_id = db.Column(db.Integer,
                        primary_key=True.
                        autoincrement=True,
                        db.ForeignKey('completions.goal_id'))
                        #DOUBLE CHECK THIS RELATIONSHIP AFTER COMPLETION
                        #TABLE CREATED!
    description = db.Column(db.,
                            nullable=False)
    ###FIX ME --> Use db.string(big number) or something else? Is there
    #a text? 


    #From the users table, users_id is a foreign key. Relationship
    #declared in User.

    #From the categories table, cat_id is a foreign key. Relationship
    #declared in Category. !!!!THIS NEEDS TO BE DONE!!!!

    num_of_times = db.Column(db.Integer,
                            nullable=False)
    time_period = db.Column(db.Integer,
                            nullable= False
                            default=7)
    ##Time_period unit is in DAYS.


    #Relationship Notes:
    #In users table backref to goals table declared.

    completions = db.relationship('Completion', backref="goals")






    








def init_app():
    from flask import Flask
    app = Flask(__name__)

    connect_to_db(app)
    print "Connected to DB."


def connect_to_db(app):
    """Connect the database to our Flask app."""

    # Configure to use our database
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