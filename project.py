
import tabloo
import pandas as pd
import time

# Getting Start time of program
start = time.time()


"""

REDUCING DATA

"""

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

