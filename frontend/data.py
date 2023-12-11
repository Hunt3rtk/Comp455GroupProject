# importing flask
from flask import Flask, render_template, request, url_for
import time

# importing postgres python api
import psycopg2

# importing pandas module
import pandas as pd

global page
global index
global data
global cursor

app = Flask(__name__)


# connect to postgres database server
def connect():
    conn = psycopg2.connect(
        user="postgres",
        password="postgres",
        host="db",
        database="database",
        port="5432"
    )
    return conn.cursor()


# create database for csv
def csv_to_db(url, cursor):
    cursor.execute("CREATE TABLE flights (legId VARCHAR(255),flightDate VARCHAR(255),startingAirport VARCHAR(255),destinationAirport VARCHAR(255), travelDuration VARCHAR(255), isBasicEconomy BOOLEAN, isRefundable BOOLEAN, isNonStop BOOLEAN, totalFare int, seatsRemaining int)")
    cursor.execute("SELECT * FROM flights")
    sqlstr = "COPY flights FROM STDIN DELIMITER ',' CSV"
    with open(url) as csv:
        cursor.copy_expert(sqlstr, csv)
    cursor.commit()
    return


url = "/app/itineraries.csv"
test = connect()


csv_to_db(url, test)


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
