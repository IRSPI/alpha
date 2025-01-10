"""
NAME:          database\controllers.py
AUTHOR:        Alan Davies (Lecturer Health Data Science)
EMAIL:         alan.davies-2@manchester.ac.uk
DATE:          17/12/2019
INSTITUTION:   University of Manchester (FBMH)
DESCRIPTION:   Contains the Database class that contains all the methods used for accessing the database
"""

from sqlalchemy.sql import func, desc, distinct
from flask import Blueprint

from app import db
from app.database.models import PrescribingData, PracticeData

database = Blueprint('dbutils', __name__, url_prefix='/dbutils')

class Database:
    """Class for managing database queries."""
    
    def convert_tuple_list_to_raw(self, tuple_list):
        """Helper function to convert results from tuple list to plain list."""
        order_row = [tuple(row) for row in tuple_list]
        return  [item for i in order_row for item in i]
    
    def get_total_number_items(self):
        """Return the total number of prescribed items."""
        return int(db.session.execute(db.select(func.sum(PrescribingData.items))).first()[0])

    def get_avg_act(self):
        "Returns average ACT cost"
        average_cost = db.session.execute(db.select(func.avg(PrescribingData.ACT_cost))).first()[0]
        return round(average_cost, 2)  # Round the average to 2 decimal places

    def get_total_drug_cost(self):
        "Returns sum of ACT cost"
        total_drug_cost = db.session.execute(db.select(func.sum(PrescribingData.ACT_cost))).first()[0]
        return round(total_drug_cost, 2)  # Round the average to 2 decimal places

    def get_max_quant_and_percentage(self):
        """
        Returns the item (BNFNAME) with the highest total quantity and the percentage
        this total is of the quantity of all prescriptions.
        """
        # Calculate the overall total quantity
        quant_sum = db.session.execute(
            db.select(func.sum(PrescribingData.quantity))
        ).scalar()

        # Calculate total quantities for each BNFNAME
        total_quantities = db.session.execute(
            db.select(
                PrescribingData.BNF_name,
                func.sum(PrescribingData.quantity).label('TotalQuantity')
            ).group_by(PrescribingData.BNF_name)
            .order_by(desc('TotalQuantity'))
        ).fetchall()

        # Get the item with the highest total quantity
        top_item = total_quantities[0]
        quant_name = top_item[0]
        quant_max = top_item[1]

        # Calculate the percentage
        quant_perc = round(quant_max * 100 / quant_sum, 2)

        return quant_name, quant_perc

    def get_num_unique(self):
        "Returns average ACT cost"
        total_rows = db.session.execute(
        db.select(func.count(distinct(PrescribingData.BNF_code)))).scalar()
        return int(total_rows)


    def get_prescribed_items_per_pct(self):
        """Return the total items per PCT."""
        result = db.session.execute(db.select(func.sum(PrescribingData.items).label('item_sum')).group_by(PrescribingData.PCT)).all()
        return self.convert_tuple_list_to_raw(result)

    def get_distinct_pcts(self):
        """Return the distinct PCT codes."""
        result = db.session.execute(db.select(PrescribingData.PCT).distinct()).all()
        return self.convert_tuple_list_to_raw(result)

    def get_n_data_for_PCT(self, pct, n):
        """Return all the data for a given PCT."""
        return db.session.query(PrescribingData).filter(PrescribingData.PCT == pct).limit(n).all()