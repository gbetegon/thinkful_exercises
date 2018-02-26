import sqlite3 as lite
import requests
from pandas.io.json import json_normalize
import time
from dateutil.parser import parse
import collections
import pandas as pd
import datetime
import matplotlib.pyplot as plt

## 1. BUILD STRUCTURE

# Access citibike URL and create DataFrame containing the information about the stations

r = requests.get('http://www.citibikenyc.com/stations/json')
df = json_normalize(r.json()['stationBeanList'])

# Create database and tables structure

station_ids = df['id'].tolist()
station_ids = ['_' + str(x) + ' INT' for x in station_ids]

con = lite.connect('citi_bike.db')
cur = con.cursor()

with con:
	cur.execute('CREATE TABLE citibike_reference (id INT PRIMARY KEY, totalDocks INT, city TEXT, altitude INT, stAddress2 TEXT, longitude NUMERIC, postalCode TEXT, testStation TEXT, stAddress1 TEXT, stationName TEXT, landMark TEXT, latitude NUMERIC, location TEXT )')
	cur.execute("CREATE TABLE available_bikes ( execution_time INT, " +  ", ".join(station_ids) + ");")

# Populate static information for citibke_reference table

sql = "INSERT INTO citibike_reference (id, totalDocks, city, altitude, stAddress2, longitude, postalCode, testStation, stAddress1, stationName, landMark, latitude, location) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)"

with con:
    for station in r.json()['stationBeanList']:
        cur.execute(sql,(station['id'],station['totalDocks'],station['city'],station['altitude'],station['stAddress2'],station['longitude'],station['postalCode'],station['testStation'],station['stAddress1'],station['stationName'],station['landMark'],station['latitude'],station['location']))

# Populate dynamic data for available_bikes.db - This is the part of the code that we need to run every minute for an hour
min_run = 0
running = True

while running:
	if min_run < 60:
		r = requests.get('http://www.citibikenyc.com/stations/json')
		df = json_normalize(r.json()['stationBeanList'])
		exec_time = parse(r.json()['executionTime'])
		with con:
			cur.execute('INSERT INTO available_bikes (execution_time) VALUES (?)', (exec_time.strftime('%s'),))

		id_bikes = collections.defaultdict(int)
		for station in r.json()['stationBeanList']:
			id_bikes[station['id']] = station['availableBikes'] #Question: not fully sure about this. Try if enough time
		with con:
			for k, v in id_bikes.iteritems():
				cur.execute("UPDATE available_bikes SET _" + str(k) + " = " + str(v) + " WHERE execution_time = " + exec_time.strftime('%s') + ";") #Q1
		min_run +=1
		time.sleep(60)
	else:
		running = False
else:
	print("Data Storage Completed.")

#connect to database
con = lite.connect('citi_bike.db')
cur = con.cursor()

# read data to DataFrame:

df = pd.read_sql_query("SELECT * FROM available_bikes ORDER BY execution_time",con,index_col='execution_time')

# store activity by station

hour_change = collections.defaultdict(int)
for col in df.columns:
	station_vals = df[col].tolist()
	station_id = col[1:]
	station_change = 0
	for k, v in enumerate(station_vals):
		if k < len(station_vals) - 1:
			station_change += abs(station_vals[k] - station_vals[k+1])
	hour_change[int(station_id)] = station_change

# find station with the most activity

def keywithmaxval(d):
	"""Find the key with the greatest value"""
	return max(d, key=lambda k: d[k])

max_station = keywithmaxval(hour_change)

cur.execute("SELECT id, stationname, latitude, longitude FROM citibike_reference WHERE id = ?", (max_station,))
data = cur.fetchone()
print("The most active station is station id %s at %s latitude: %s longitude: %s " % data)
print("With %d bicycles coming and going in the hour between %s and %s" % (
	hour_change[max_station],
	datetime.datetime.fromtimestamp(int(df.index[0])).strftime('%Y-%m-%dT%H:%M:%S'),
	datetime.datetime.fromtimestamp(int(df.index[-1])).strftime('%Y-%m-%dT%H:%M:%S'),
	))

plt.bar(hour_change.keys(), hour_change.values())
plt.show()



