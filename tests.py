"""Unittest for flask and database on goal_tracker app"""

import unittest
import server


class GoalTrackerTests(unittest.TestCase):
    """Tests for goal_tracker site."""

    def setUp(self):
        self.client = app.test_client()
        server.app.config['TESTING'] = True

    def test_hompage(self):
        result = self.client.get("/")





if __name__ = '__main__':
    unittest.main()