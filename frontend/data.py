# importing flask
from flask import Flask, render_template, request, url_for
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


# create database for csv
def csv_to_db(url, cursor, table_name):
    cursor.execute(f"CREATE TABLE {table_name} ()")  # create empty table
    query = ""
    for header in headers:
        query = (
            f"ALTER TABLE {table_name} ADD COLUMN {header} TEXT"  # add column to table
        )
        cursor.execute(query)
    cursor.execute(f"SELECT * FROM {table_name}")
    sqlstr = f"COPY {table_name} FROM STDIN DELIMITER ',' CSV HEADER"
    with open(url) as csv:
        cursor.copy_expert(sqlstr, csv)
    conn.commit()
    return


def build_query_string(columns, search_term, order_by_column, limit):
    query_string = f"SELECT {columns} "
    query_string += f"FROM {table_name} "
    query_string += "WHERE "
    if isinstance(columns, list):  # if columns is a string, only search that column
        query_string += " OR ".join(  # if columns is a list, search all columns
            [f"{column} LIKE '%{search_term}%'" for column in columns]
        )
    else:
        query_string += f"{columns} LIKE '%{search_term}%'"
    query_string += " "
    query_string += f"ORDER BY {order_by_column} "
    query_string += f"LIMIT {limit}"
    return query_string


@app.route("/")
def index():
    return render_template("index.html", titles=headers, table_name=table_name)


@app.route("/search")
def search():
    search_term = request.args.get("search_term")
    if request.args.get("scope") == "all":
        scope = ', '.join(str(header) for header in headers)
    else:
        scope = request.args.get("scope")
    sorted_by = request.args.get("sorted")
    limit = request.args.get("limit")

    query = build_query_string(scope, search_term, sorted_by, limit)
    cursor.execute(query)
    result = cursor.fetchall()

    return render_template("search_results.html", results=result)


conn = psycopg2.connect(
    user="postgres",
    password="postgres",
    host="db",
    database="postgres",
    port="5432",
)
cursor = conn.cursor()

csv_folder = "data/"
csv_files = os.listdir(csv_folder)
for csv_file in csv_files:
    url = csv_folder + csv_file
df = pd.read_csv(url, nrows=2)
headers = df.columns.tolist()
headers = [re.sub(r"\W+", "", header) for header in headers]
filename = os.path.basename(url)
table_name = os.path.splitext(filename)[0].lower()  # create table name from filename
csv_to_db(url, cursor, table_name)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
