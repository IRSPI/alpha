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
        self.client = self.app.test_client()  # Create a test client

    def tearDown(self):
        """Run post each test."""
        # Pop the application context
        self.app_context.pop()

    def test_404_error_handler(self):
        """Test the 404 error handler."""
        # Test client will request a non-existent route
        response = self.client.get('/non-existent-route')
        self.assertEqual(response.status_code, 404)
        self.assertIn(b'<h1>Page not found</h1>', response.data)

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

    def test_get_prescribed_items_per_pct(self):
        """Test the get_prescribed_items_per_pct method."""
        result = self.db_mod.get_prescribed_items_per_pct()[0]
        expected_result = 229169  # check for the first result
        self.assertEqual(result, expected_result)

    def test_distinct_pcts(self):
        "Test that the number of distinct PCTs is correct"
        self.assertEqual(len(self.db_mod.get_distinct_pcts()), 34)

    def test_get_n_data_for_PCT(self):
        """Test the get_n_data_for_PCT method."""
        result = self.db_mod.get_n_data_for_PCT('00C', 5)
        expected_result = 5
        self.assertEqual(len(result), expected_result)

class ViewTests(unittest.TestCase):
    """Class for testing"""

    def setUp(self):
        """Set up before each test."""
        # Tell Flask to use the app
        self.app = app
        self.app_context = self.app.app_context()  # Create app context
        self.app_context.push()  # Activate the context
        self.client = self.app.test_client()  # Create a test client
        self.client.testing = True  # Set the testing flag to True to enable error propagation

    def tearDown(self):
        """Run after each test."""
        # Pop the application context
        self.app_context.pop()

    def test_home_get(self):
        """Test the home page for GET request."""
        response = self.client.get('/dashboard/home/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'<select', response.data)  # Replace with an actual string found on the home page, like 'Dashboard'
        self.assertIn(b'111', response.data)  # Ensure the pct_list is passed to the template (this assumes it's rendered as part of the HTML)

    def test_home_post(self):
        """Test the home page for POST request."""
        # Simulate selecting a PCT and submitting the form
        form_data = {
            'pct-option': '111'  # Replace with an actual PCT value from your database
        }
        response = self.client.post('/dashboard/home/', data=form_data)
        self.assertEqual(response.status_code, 200)

        # Check if the response contains the updated data
        self.assertIn(b'<tr>', response.data)  # Assuming the selected PCT data is rendered in the template
        self.assertIn(b"111", response.data)  # Verify that the selected PCT is in the response


if __name__ == "__main__":  # pragma: no cover
    unittest.main()

