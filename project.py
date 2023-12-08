
import tabloo
import pandas as pd

"""

REDUCING DATA

"""

# GET CSV
# Reducing the 27 column csv into 10 columns
csv = pd.read_csv("itineraries.csv", chunksize=5000, nrows=800000, usecols=['legId', 'flightDate', 'startingAirport', 'destinationAirport', 'travelDuration', 'isBasicEconomy', 'isRefundable', 'isNonStop', 'totalFare', 'seatsRemaining'])
csv = pd.concat(csv, ignore_index=True)


# Deleting flights with no empty seats
csv = csv[csv.seatsRemaining != 0]

# Only displaying the cheapest filght from A to B
# csv = csv.groupby(['startingAirport', 'destinationAirport']).min()
# csv['totalFare'] = csv.groupby(['startingAirport', 'destinationAirport'])['totalFare'].min()


# Display
tabloo.show(csv)