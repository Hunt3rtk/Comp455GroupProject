# importing flask
from flask import Flask, render_template, url_for
from sqlalchemy import create_engine, text

# importing pandas module
import pandas as pd

global page
global index
global dataArray

app = Flask(__name__)

# converting csv to html
data = pd.read_csv(
    "itineraries.csv",
    chunksize=5000,
    nrows=10000,
    usecols=[
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
    ],
)
data = pd.concat(data, ignore_index=True)

# splitting the csv int chunks for pages
dataArray = [data[i : i + 100] for i in range(0, len(data), 50)]
dataArray = [df.to_html() for df in dataArray]

engine = create_engine("sqlite+pysqlite:///:memory:")
data.to_sql("flights", engine)


# route to html page - "table"
@app.route("/")
@app.route("/table")
def table():
    return render_template("table.html", tables=dataArray, page=1, index=0, titles=[""])


# route to reset tables with filters applied
@app.route("/table_reset")
def page_reset():
    print("yup", flush="True")
    return


# route to update page to next table
@app.route("/next_page/<int:page>/<int:index>", methods=["POST"])
def next_page(index, page):
    ind = index + 1
    pg = page + 1
    return render_template(
        "table.html", tables=dataArray, page=pg, index=ind, titles=[""]
    )


@app.route("/select_column/")
def select_column():
    c = request.args.get("c")  # return the query as q
    with engine.connect() as conn:
        # let's select the column credit_history
        # from the loan data table
        result = conn.execute(text(f"SELECT {c} FROM flights"))
    return render_template("table.html", tables=result, page=1, index=0, titles=[""])


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
