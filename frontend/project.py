import tkinter as tk
from tkinter import ttk
import pysolr

# Creating a lil gui using tkinter
window = tk.Tk()
file = "intinerary.csv"
window.geometry("800x600")
window.title(f"Search through {file}")
table = pysolr.Solr("http://localhost:8983/solr/itinerary", always_commit=True)
# something like this to connect to the solr server, idk I haven't installed solr yet


# Idk if this even works,  but it should get the column names from the schema
# It should return them as a comma separated string, which is what we need
columns = table.schema.get_field_names()
# if not, lets try this, appending this string, found it on stackoverflow "select?q=*:*&wt=csv&rows=0&facet"


# Create a treeview widget to display a table
tree = ttk.Treeview(
    window,  # Parent
    columns,  # Columns
    show="headings",  # Hide the default column
)

# Scrollbars because length might be long asl and width might also be long asl
vsb = ttk.Scrollbar(window, orient="vertical", command=tree.yview)
vsb.pack(side="right", fill="y")
hsb = ttk.Scrollbar(window, orient="horizontal", command=tree.xview)
hsb.pack(side="bottom", fill="x")
tree.configure(yscrollcommand=vsb.set)

# Define the column headings
for col in columns:
    tree.heading(col, text=col)
tree.pack()


# tree.insert("", "end", values=())


window.mainloop()  # init the window innit

"""
 Hunters Code for reference, might be useful when we figure out solr

 import tabloo
 import pandas as pd
 import time

 # Getting Start time of program
 start = time.time()

 REDUCING DATA

 # GET CSV
 # Reducing the 27 column csv into 10 columns
 csv = pd.read_csv("itineraries.csv", chunksize=5000, nrows=1000000, usecols=['legId', 'flightDate', 'startingAirport', 'destinationAirport', 'travelDuration', 'isBasicEconomy', 'isRefundable', 'isNonStop', 'totalFare', 'seatsRemaining'])
 csv = pd.concat(csv, ignore_index=True)

 # Deleting flights with no empty seats
 csv = csv[csv.seatsRemaining != 0]

 # Only displaying the cheapest filght from A to B on each day
 csv = csv.sort_values(by='totalFare', ascending=True)
 csv = csv.drop_duplicates(subset=['startingAirport', 'destinationAirport', 'flightDate'], keep='first')

 # Output program run-time
 print(round((time.time() - start),3), 'seconds', flush='True')

 # Display
 tabloo.show(csv)

"""
