# importing flask
from flask import Flask, render_template, request, url_for
import time
import re
import os

# importing postgres python api
import psycopg2

# importing pandas module
import pandas as pd

global data
global table_name
global cursor

app = Flask(__name__)


# connect to postgres database server
conn = psycopg2.connect(
    user="postgres",
    password="postgres",
    host="db",
    database="postgres",
    port="5432",
)
cursor = conn.cursor()


# create database for csv
def csv_to_db(url, cursor):
    df = pd.read_csv(url, nrows=2)
    headers = df.columns.tolist()  # get the headers of each column
    dtypes = df.dtypes.map(lambda x: x.name)  # get the data type of each column

    dtypeLookup = {
        "int64": "INT",
        "float64": "FLOAT",
        "object": "TEXT",
        "bool": "BOOLEAN",
    }
    filename = os.path.basename(url)
    table_name = os.path.splitext(filename)[0]
    cursor.execute(f"CREATE TABLE {table_name} ()")  # create table dynamically
    query = ""
    for i, header in enumerate(headers):
        header = re.sub("[^0-9a-zA-Z_]+", "_", header)
        query = f"ALTER TABLE {table_name} ADD COLUMN {header} TEXT"
        print(query)
        cursor.execute(query)
    cursor.execute(f"SELECT * FROM {table_name}")
    sqlstr = f"COPY {table_name} FROM STDIN DELIMITER ',' CSV"
    with open(url) as csv:
        cursor.copy_expert(sqlstr, csv)
    conn.commit()
    return


csv_folder = "data/"
csv_files = os.listdir(csv_folder)
for csv_file in csv_files:
    url = csv_folder + csv_file
csv_to_db(url, cursor)


# route to html page - "table"
@app.route("/")
@app.route("/table")
def table():
    cursor.execute("SELECT * FROM {table_name} LIMIT 50")
    data = cursor.fetchall()
    return render_template("table.html", tables=data, titles=[""])


@app.route("/select_column/")
def select_column():
    q = request.args.get("q")  # return the query as q
    cursor.execute("SELECT {q} FROM {table_name}")
    data = cursor.fetchall()

    return render_template("table.html", tables=data, titles=[""])


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
