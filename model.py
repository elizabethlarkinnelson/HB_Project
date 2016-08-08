"""Models and db functions for goal_tracker db"""

from flask_sqlalchemy import SQLAlchemy


#Creating the session object where we can preform transactions.
db = SQLAlchemy()


#Composing Object Relation Models(ORM) 

#Creating first table named "users"
class User(db.):










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