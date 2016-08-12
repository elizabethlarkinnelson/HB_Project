"""Unittest for flask and database on goal_tracker app"""

import unittest
import server



class GoalTrackerTests(unittest.TestCase):
    """Tests for goal_tracker site."""

    def setUp(self):
        self.client = server.app.test_client()
        server.app.config['TESTING'] = True

    def test_homepage(self):
        result = self.client.get("/")
        self.assertIn("New", result.data)

    # def test_user_goals(self):
    #     result = self.client.get("/user/<int:user_id>")








if __name__ == '__main__':
    unittest.main()