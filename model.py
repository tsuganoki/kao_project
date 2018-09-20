"""Models and database functions for Tilia's project."""

from flask_sqlalchemy import SQLAlchemy
import datetime
# This is the connection to the PostgreSQL database; we're getting this through
# the Flask-SQLAlchemy helper library. On this, we can find the `session`
# object, where we do most of our interactions (like committing, etc.)

db = SQLAlchemy()


##############################################################################
# Model definitions

class User(db.Model):
    """User of to-do website."""

    __tablename__ = "users"

    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    username = db.Column(db.String(64), unique=True)
    email = db.Column(db.String(64), nullable=False, unique=True)
    password = db.Column(db.String(64), nullable=False)
    timezone = db.Column(db.String(32), default="US/Pacific")
    
    def __repr__(self):
        """Provide helpful representation when printed."""
        return f"<User user_id={self.user_id} email={self.email}>"

class Task(db.Model):
	"""tasks stored in to-do website"""

	__tablename__ = "tasks"

	task_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
	msg = db.Column(db.String(264))
	user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
	is_complete = db.Column(db.Boolean, nullable=False, default=False)
	is_repeating = db.Column(db.Boolean, default=False)
	due_date = db.Column(db.DateTime, default=False)


	def __repr__(self):
		return f"<Task task_id {self.task_id} msg {self.msg[:16]}>"


	user = db.relationship("User", backref=db.backref("tasks", order_by=task_id))


class Collect(db.Model):
	"""Kao-moji collected by users"""

	__tablename__ = "collects"

	collect_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
	user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
	kao_id = db.Column(db.Integer, db.ForeignKey('kaos.kao_id'))
	collect_date = db.Column(db.DateTime)

	def __repr__(self):
		"""Provide helpful representation when printed."""
		return f"<Collects collect_id={self.collect_id} user_id={self.user_id}>"

	kaos = db.relationship("Kao",backref=db.backref("collects",order_by=collect_id))



class Kao(db.Model):
	"""unicode kaomoji and their ids"""

	__tablename__ = "kaos"

	kao_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
	kao = db.Column(db.String(64),nullable=False)


##############################################################################
# Helper functions

def example_data():
    """Create some sample data."""

    # In case this is run more than once, empty out existing data
    User.query.delete()
    Task.query.delete()

    # Add sample employees and departments
    bob = User(username='bobrules', email='bob@gmail.com', password='abc123', timezone="US/Pacific")
    qian = User(username='qian', email='qian@weibo.cn', password='YarHekjanyighd1', timezone="Asia/Taipei")
    tilia = User(username='tilia', email='somedude@tilia.com', password='kaosrgreat', timezone="US/Pacific")

    starworld = Task(msg='make the phone call to Starworld Advertising', user_id=bob,
			is_complete=False, is_repeating=False, due_date=(datetime.datetime(2018,9,30,7)))
    bao = Task(msg='eat bao', user_id=qian, 
			is_complete=False, is_repeating=False, due_date=(datetime.datetime(2018,9,30,16)))
    kao = Task(msg='write Kao selection features', user_id=tilia, 
			is_complete=False, is_repeating=False, due_date=(datetime.datetime(2018,10,30,7)))
    tilia_tests = Task(msg='write some tests', user_id=tilia, 
			is_complete=False, is_repeating=False, due_date=(datetime.datetime(2018,10,7,7)))

    db.session.add_all([bob, qian, tilia, starworld, bao, kao, tilia_tests])
    db.session.commit()

def connect_to_db(app, db_uri='postgresql:///kao_project'):
    """Connect the database to our Flask app."""

    # Configure to use our PstgreSQL database
    app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app
    db.init_app(app)


if __name__ == "__main__":
    # As a convenience, if we run this module interactively, it will leave
    # you in a state of being able to work with the database directly.

    from server import app
    connect_to_db(app)
    print("Connected to DB.")
