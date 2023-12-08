#!/bin/python3

from flask import Flask, render_template, request  # pip3 install flask
from flask_sqlalchemy import SQLAlchemy  # pip3 install flask_sqlalchemy
import csv


app = Flask(__name__)
db = SQLAlchemy()


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/search")
def search():
    return render_template("search.html")


def load_data():
    flight_data = {}
    with open("itineraries.csv") as f:
        reader = csv.DictReader(f)
        for row in reader:
            flight_data[row["id"]] = row
    return flight_data


app.run(host="0.0.0.0", debug=True, threaded=True, use_reloader=False)
