# importing flask
from flask import Flask, render_template, request, url_for
# importing postgres python api
import psycopg
# importing pandas module
import pandas as pd

global page
global index
global data
global cursor

app = Flask(__name__)

# connect to postgres database server
def connect():

    conn = psycopg.connect(
        user="postgres",
        password="postgres",
        host="localhost:5432",
    )
    return conn.cursor()

# create database for csv
def csv_to_db(url, cursor):
    cursor.execute("""
        CREATE TABLE flights
    """)
    cursor.copy_from(url, 'flights', sep=',', columns=[
        "legId",
        "flightDate",
        "startingAirport",
        "destinationAirport",
        "travelDuration",
        "isBasicEconomy",
        "isRefundable",
        "isNonStop",
        "totalFare",
        "seatsRemaining",
    ],)
    cursor.commit()
    return


cursor = connect()
url = '/frontend/itineraries.csv'

csv_to_db(url, cursor)


# route to html page - "table"
@app.route("/")
@app.route("/table")
def table():
    cursor.execute("SELECT * FROM flights")
    data = cursor.fetchmany(100000)
    return render_template("table.html", tables=data, page=1, index=0, titles=[""])

# route to update page to next table
# @app.route("/next_page/<int:page>/<int:index>", methods=["POST"])
# def next_page(index, page):
#    ind = index + 1
#    pg = page + 1
#    return render_template(
#        "table.html", tables=data, page=pg, index=ind, titles=[""]
#    )


@app.route("/select_column/")
def select_column():
    q = request.args.get("q")  # return the query as q
    cursor.execute("SELECT {q} FROM flights")
    data = cursor.fetchmany(100000)

    return render_template("table.html", tables=data, page=1, index=0, titles=[""])


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
