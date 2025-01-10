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
        self.assertEqual(self.db_mod.get_total_number_items(),8218165,)
        'Test total items returns correct value'
        self.assertEqual(self.db_mod.get_avg_act(),76.22,)
        self.assertEqual(self.db_mod.get_num_unique(), 13935, )

    def test_total_drug_cost (self):
        "Test that the total drug cost is correct"
        self.assertEqual(self.db_mod.get_total_drug_cost(), 60316449.37, )

    def test_avg_act (self):
        "Test that the average ACT is correct"
        self.assertEqual(self.db_mod.get_avg_act(), 76.22, )

    def test_max_item_and_percent (self):
        "Testing to find the percentage of the item with the highest quantity is correct"
        quant_name, quant_perc = self.db_mod.get_max_quant_and_percentage()
        self.assertEqual(quant_name, "Ensure Plus_Milkshake Style Liq (9 Flav)", )
        self.assertEqual(quant_perc, 2.98, )

    def test_num_unique (self):
        "Test that the number of unique items is correct"
        self.assertEqual(self.db_mod.get_num_unique(), 13935, )

    '''missing def test_prescribed_item_per_pct(self):'''

    def test_distinct_pcts(self):
        "Test that the number of distinct PCTs is correct"
        self.assertEqual(len(self.db_mod.get_distinct_pcts()), 34)

    '''missing def test_n_data_for_PCT(self, pct, n):'''

if __name__ == "__main__":
    unittest.main()

