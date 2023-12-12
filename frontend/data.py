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
    filename = os.path.basename(url)
    table_name = os.path.splitext(filename)[
        0
    ].lower()  # create table name from filename
    cursor.execute(f"CREATE TABLE {table_name} ()")  # create empty table
    query = ""
    for header in headers:
        header = re.sub(
            "[^0-9a-zA-Z_]+", "_", header
        )  # replace special characters with underscores
        query = (
            f"ALTER TABLE {table_name} ADD COLUMN {header} TEXT"  # add column to table
        )
        cursor.execute(query)
    cursor.execute(f"SELECT * FROM {table_name}")
    sqlstr = f"COPY {table_name} FROM STDIN DELIMITER ',' CSV  HEADER"
    with open(url) as csv:
        cursor.copy_expert(sqlstr, csv)
    conn.commit()
    return table_name


def build_query_string(columns, search_term, order_by_column, limit):
    query_string = f"SELECT {columns}\n"
    query_string += f"FROM {table_name}\n"
    query_string += "WHERE ("
    if isinstance(columns, str):  # if columns is a string, only search that column
        query_string += f"\"{columns}\" LIKE '%{search_term}%'"
    else:
        query_string += " OR ".join(  # if columns is a list, search all columns
            [f"\"{column}\" LIKE '%{search_term}%'" for column in columns]
        )
    query_string += ")\n"
    query_string += f'ORDER BY "{order_by_column}"\n'
    query_string += f"LIMIT {limit}"
    return query_string


csv_folder = "data/"
csv_files = os.listdir(csv_folder)
for csv_file in csv_files:
    url = csv_folder + csv_file
df = pd.read_csv(url, nrows=2)
headers = df.columns.tolist()
table_name = csv_to_db(url, cursor)


@app.route("/")
def table():
    cursor.execute(f"SELECT * FROM {table_name} LIMIT 50")
    data = cursor.fetchall()  # initial data display
    return render_template(
        "index.html", tables=data, titles=headers, table_name=table_name
    )


@app.route("/search")
def search():
    search_term = request.args.get("search_term")

    scope = (
        headers if request.args.get("scope") == "all" else {request.args.get("scope")}
    )
    sorted_by = request.args.get("sorted")
    limit = request.args.get("limit")

    query = build_query_string(scope, search_term, sorted_by, limit)
    print(query)
    print(f"Search: {search_term}")
    print(f"Scope: {scope}")
    print(f"Sorted by: {sorted_by}")
    print(f"Limit: {limit}")
    cursor.execute(query)
    result = cursor.fetchall()
    result = []

    return render_template("search_results.html", results=result)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
