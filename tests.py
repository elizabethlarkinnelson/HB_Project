"""Unittest for flask and database on goal_tracker app"""

import unittest
import server



class GoalTrackerTests(unittest.TestCase):
    """Tests for goal_tracker site."""

    def setUp(self):
        """Stuff to do before every test."""
        self.client = server.app.test_client()
        server.app.config['TESTING'] = True

    def test_homepage(self):
        result = self.client.get("/")
        self.assertIn("New", result.data)

    # def test_user_goals(self):
    #     result = self.client.get("/user/<int:user_id>")
    #FIXME!!!!!!!


class GoalTrackerDatabse(unittest.TestCase):
    """Flask tests the use of the database"""

    def setUp(self):
        """Stuff to do before every test."""
        self.client = server.app.test_client()
        app.config['TESTING'] = True
        connect_to_db(server.app, "postgresql:////goal_tracker")
        db.create_all()
        example_data()
        #FIX ME!!! Still need to make example_data function
        #in model file.


    def tearDown(self):
        """To do at the end of every test."""

        db.session.close()
        db.drop_all()





if __name__ == '__main__':
    unittest.main()