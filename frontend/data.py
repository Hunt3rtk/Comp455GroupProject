# importing flask
from flask import Flask, render_template, request, url_for
import time
import re
import os

# importing postgres python api
import psycopg2

# importing pandas module
import pandas as pd

global cursor

global data
global table_name

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
    table_name = os.path.splitext(filename)[0].lower()
    cursor.execute(f"CREATE TABLE {table_name} ()")  # create table dynamically
    query = ""
    for i, header in enumerate(headers):
        header = re.sub("[^0-9a-zA-Z_]+", "_", header)
        query = f"ALTER TABLE {table_name} ADD COLUMN {header} TEXT"
        print(query)
        cursor.execute(query)
    cursor.execute(f"SELECT * FROM {table_name}")
    sqlstr = f"COPY {table_name} FROM STDIN DELIMITER ',' CSV  HEADER"
    with open(url) as csv:
        cursor.copy_expert(sqlstr, csv)
    conn.commit()
    return table_name

def build_query_string(columns, search_term, order_by_column, limit):
    query_string = f"SELECT {columns}\n"
    query_string += f'FROM "{table_name}"\n'
    query_string += "WHERE ("
    query_string += " OR ".join(
        [f"\"{column}\" LIKE '%{search_term}%'" for column in columns.split(",")]
    )
    query_string += ")\n"
    query_string += f'ORDER BY "{order_by_column}"\n'
    query_string += f"LIMIT {limit}"
    return query_string


csv_folder = "data/"
csv_files = os.listdir(csv_folder)
for csv_file in csv_files:
    url = csv_folder + csv_file
table_name = csv_to_db(url, cursor)


# route to html page - "table"
@app.route("/")
@app.route("/table")
def table():
    cursor.execute(f"SELECT * FROM {table_name} LIMIT 50")
    data = cursor.fetchall()
    return render_template("index.html", tables=data, titles=[""])


@app.route("/search")
def search():

    columns = request.args.get("columns")
    search_term = request.args.get("search_term")
    order = request.args.get("order")
    limit = request.args.get("limit")
    
    query = build_query_string(columns, search_term, order, limit)
    cursor.execute(query)
    result = cursor.fetchall()

    return render_template("search_results.html", results=result, titles=[""])


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
