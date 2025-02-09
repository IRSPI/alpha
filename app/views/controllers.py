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
import os
import plotly
import plotly.express as px
import pandas as pd
from flask import Blueprint, render_template, request,jsonify, redirect, url_for, flash, session
from flask_login import login_user, logout_user, login_required, LoginManager, current_user
from app.database.controllers import Database, register_user, authenticate_user
import logging
from app.database.models import db, User
from flask_mail import Message
from app import mail, app

views = Blueprint('dashboard', __name__, url_prefix='/dashboard')

auth = Blueprint('auth', __name__)

login_manager = LoginManager()
login_manager.login_view = "auth.login"

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@auth.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        message = register_user(username, email, password)
        flash(message)
        return redirect(url_for('auth.login'))

    return render_template('register.html')

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if 'email' not in request.form or 'password' not in request.form:
            flash("Invalid form submission. Please try again.", "danger")
            return redirect(url_for('auth.login'))

        email = request.form['email']
        password = request.form['password']
        user = authenticate_user(email, password)

        if user:
            login_user(user)
            flash("Login successful!", "success")
            return redirect(url_for('dashboard.home'))
        else:
            flash("Invalid email or password. Please try again.", "danger")

    return render_template('login.html')


@auth.route('/logout')
@login_required
def logout():
    session.pop('_flashes', None)  # Clears any existing flash messages
    logout_user()
    flash("Logged out successfully.", "info")
    return redirect(url_for('auth.login'))

@auth.route('/reset_password', methods=['GET', 'POST'])
def reset_request():
    """Allow users to request a password reset link via email."""
    if request.method == 'POST':
        email = request.form['email']
        user = User.query.filter_by(email=email).first()

        if user:
            send_reset_email(user)
            flash('An email has been sent with instructions to reset your password.', 'info')
        else:
            flash('No account found with that email.', 'danger')

    return render_template('reset_request.html')

@auth.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_token(token):
    """Allow users to reset their password after clicking the link in the email."""
    user = User.verify_reset_token(token)
    if not user:
        flash('This link is invalid or has expired.', 'danger')
        return redirect(url_for('auth.reset_request'))

    if request.method == 'POST':
        password = request.form['password']
        user.password = User.hash_password(password)
        db.session.commit()
        flash('Your password has been updated! You can now log in.', 'success')
        return redirect(url_for('auth.login'))

    return render_template('reset_password.html', token=token)


# get the database class
db_mod = Database()

# Set the route and accepted methods
@views.route('/home/', methods=['GET', 'POST'])
@login_required  # This forces login before accessing this page
def home():
    """Render the home page of the dashboard passing in data to populate dashboard."""
    pcts = db_mod.get_distinct_pcts()
    if request.method == 'POST':
        form = request.form
        selected_pct_data = db_mod.get_n_data_for_PCT(str(form['pct-option']), 5)
    else:
        selected_pct_data = db_mod.get_n_data_for_PCT(str(pcts[0]), 5)

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

    return render_template('dashboard/index.html', dashboard_data=dashboard_data)

def send_reset_email(user):
    """Send the user an email with a password reset link."""
    token = user.get_reset_token()
    reset_link = url_for('auth.reset_token', token=token, _external=True)

    msg = Message(
        'Password Reset Request',
        sender= os.getenv('EMAIL_USER'),  # Explicitly set the sender
        recipients=[user.email]
    )
    msg.body = f'''To reset your password, visit the following link:
{reset_link}

If you did not request this, please ignore this email.
'''
    mail.send(msg)



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
    """Generate the data needed to populate the opioid dependence treatment barchart."""
    # Get percentage data for each drug
    drug_percentages = db_mod.get_opioid_dependence_count()
    # Create a dataframe with drug names and their percentages
    df = pd.DataFrame({
        "drug_names": list(drug_percentages.keys()),
        "percentages": list(drug_percentages.values())
    })
    # Generate the bar chart
    fig = px.bar(df, x="drug_names", y="percentages",
                 labels={"drug_names": "Drug Name",
                         "percentages": "Percentage (%)"}).update_xaxes(categoryorder="total descending")
    # Convert the plot for rendering and add any metadata (description/header)
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    header = "Opioid Dependence Treatment Drug Distribution"
    description = "Percentage breakdown of opioid dependence treatment by drug."
    plot_data = {
        'graphJSON': graphJSON,
        'header': header,
        'description': description
    }
    return plot_data
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



