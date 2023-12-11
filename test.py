import pandas as pd


def csv_to_db(url):
    df = pd.read_csv(url, nrows=2)
    headers = df.columns.tolist()  # get the headers of each column
    dtypes = df.dtypes.map(lambda x: x.name)  # get the data type of each column
    print(df["elapsedDays"])

    dtypeLookup = {
        "int64": "INT",
        "float64": "FLOAT",
        "object": "TEXT",
        "bool": "BOOLEAN",
    }
    query = ""
    for i, header in enumerate(headers):
        if i == 0:
            query = f"ALTER TABLE flights ADD COLUMN {header} TEXT PRIMARY KEY"
        else:
            query = f"ALTER TABLE flights ADD COLUMN {header} TEXT"
        print(query)


url = "frontend/itineraries.csv"
csv_to_db(url)
