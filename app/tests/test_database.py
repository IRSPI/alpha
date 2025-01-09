"""
NAME:          test_database.py
AUTHOR:        Alan Davies (Lecturer Health Data Science)
EMAIL:         alan.davies-2@manchester.ac.uk
DATE:          24/12/2019
INSTITUTION:   University of Manchester (FBMH)
DESCRIPTION:   Suite of tests for testing the dashboards database
               functionality.
"""

import unittest
from app import app
from app.database.controllers import Database

class DatabaseTests(unittest.TestCase):
    """Class for testing database functionality and connection."""

    def setUp(self):
        """Set up before each test."""
        # Tell Flask to use the app
        self.app = app
        self.app_context = self.app.app_context()  # Create app context
        self.app_context.push()  # Activate the context
        self.db_mod = Database()  # Create the database instance

    def tearDown(self):
        """Run post each test."""
        # Pop the application context
        self.app_context.pop()

    def test_get_total_number_items(self):
        """Test that the total number of items returns the correct value."""
        quant_name, quant_perc = self.db_mod.get_max_quant_and_percentage()
        self.assertEqual(self.db_mod.get_total_number_items(),8218165,)
        'Test total items returns correct value'
        self.assertEqual(self.db_mod.get_avg_act(),76.22,)
        self.assertEqual(quant_name, "Methadone HCl_Oral Soln 1mg/1ml S/F", )
        self.assertEqual(quant_perc, 0.14, )
        self.assertEqual(self.db_mod.get_num_unique(), 791341, )


if __name__ == "__main__":
    unittest.main()

if __name__ == "__main__":
    unittest.main()