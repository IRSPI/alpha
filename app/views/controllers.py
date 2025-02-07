"""
NAME:          views\controllers.py
AUTHOR:        Alan Davies (Senior Lecturer Health Data Science)
EMAIL:         alan.davies-2@manchester.ac.uk
DATE:          18/12/2019
UPDATED:       07/06/2024
INSTITUTION:   University of Manchester (FBMH)
DESCRIPTION:   Views module. Renders HTML pages and passes in associated data to render on the
               dashboard.
"""
import json
import plotly
import plotly.express as px
import pandas as pd
from flask import Blueprint, render_template, request,jsonify
from app.database.controllers import Database
import logging

views = Blueprint('dashboard', __name__, url_prefix='/dashboard')

# get the database class
db_mod = Database()

# Set the route and accepted methods
@views.route('/home/', methods=['GET', 'POST'])
def home():
    """Render the home page of the dashboard passing in data to populate dashboard."""
    pcts = db_mod.get_distinct_pcts()
    if request.method == 'POST':
        # if selecting PCT for table, update based on user choice
        form = request.form
        selected_pct_data = db_mod.get_n_data_for_PCT(str(form['pct-option']), 5)
    else:
        # pick a default PCT to show
        selected_pct_data = db_mod.get_n_data_for_PCT(str(pcts[0]), 5)

    # prepare data structure to send to front end to update display
    dashboard_data = {    
        "tile_data_items": generate_data_for_tiles(),  
        "top_items_plot_data": generate_top_px_items_barchart_data(),
        "pct_list": pcts,
        "pct_data": selected_pct_data,
        "top_pct_with_most_practices": get_pct_with_most_practices(),
        "num_practices": get_num_practices_for_pct(get_pct_with_most_practices()),
        "infection_drug_data": generate_infection_drug_data(),
        "opioid_dependence_data": generate_opioid_dependence_data(),
    }

    # render the HTML page passing in relevant data
    return render_template('dashboard/index.html',dashboard_data=dashboard_data)


def generate_data_for_tiles():
    """Generate the data for the four home page tiles."""
    quant_name, quant_perc = db_mod.get_max_quant_and_percentage()
    tile_data = {
        "total_items": db_mod.get_total_number_items(),
        "avg_act_cost": db_mod.get_avg_act(),
        "total_drug_cost": db_mod.get_total_drug_cost(),
        "top_px_item": quant_name,
        "top_px_perc": quant_perc,
        "num_unique_items": db_mod.get_num_unique()
    }
    return tile_data

def generate_top_px_items_barchart_data():
    """Generate the data needed to populate the number of most prescrbed items per PCT barchart."""

    # Create a dataframe to store the database query results
    df = pd.DataFrame({
        "data_values": db_mod.get_prescribed_items_per_pct(),
        "pct_codes": db_mod.get_distinct_pcts()
    })
    # Generate the plot
    fig = px.bar(df, x="pct_codes", y="data_values",
                 labels={"pct_codes": "PCT code",
                         "data_values": "Prescribed items (number)"}).update_xaxes(categoryorder="sum descending")

    # Convert the plot for rendering and add any metadata (description/header)
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    header="Prescribed items per Primary Care Trust (PCT)"
    description = "Total number (sum) of prescribed items per PCT (Primary Care Trust) by PCT code."
    plot_data = {
        'graphJSON': graphJSON,
        'header': header,
        'description': description
    }
    return plot_data

def generate_infection_drug_data():
    counts = db_mod.get_infection_drug_count()

    labels = ["Antibacterials", "Antifungal", "Antiviral", "Antiprotozoal", "Anthelmintics"]
    values = [counts['0501'], counts['0502'], counts['0503'], counts['0504'], counts['0505']]

    fig = px.pie(values=values, names=labels, title="Percentage of infection drug use by BNF Code")
    fig.update_traces(textinfo='percent+label')

    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    header = "Percentage of infection drug use"
    description = "Pie chart showing the percentage of infection drug use by BNF code."
    plot_data = {
        'graphJSON': graphJSON,
        'header': header,
        'description': description
    }
    # Debug statement
    logging.debug(f"Generated plot data: {plot_data}")

    return plot_data


def get_pct_with_most_practices():
    """Get the PCT code that contains the most GP practices."""
    pct_code, _ = db_mod.get_pct_with_most_gp_practices()
    return pct_code

def get_num_practices_for_pct(pct_code):
    """Get the number of GP practices for a given PCT code."""
    _, num_practices = db_mod.get_pct_with_most_gp_practices()
    return num_practices

def generate_opioid_dependence_data():
    counts = db_mod.get_opioid_dependence_count()

    labels = ["Buprenorphine", "Lofexidine", "Methadone", "Naltrexone"]
    values = [counts['Buprenorphine'], counts['Lofexidine'], counts['Methadone'], counts['Naltrexone']]

    fig1 = px.pie(values=values, names=labels, title="Percentage of Opioid dependence by BNF Name")
    fig1.update_traces(textinfo='percent+label')

    graphJSON1 = json.dumps(fig1, cls=plotly.utils.PlotlyJSONEncoder)
    header1 = "Percentage of Opioid dependence "
    description1 = "Pie chart showing the Opioid dependence by BNF name."
    plot_data1 = {
        'graphJSON': graphJSON1,
        'header': header1,
        'description': description1
    }
    # Debug statement
    logging.debug(f"Generated plot data: {plot_data1}")

    return plot_data1


