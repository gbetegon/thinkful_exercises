import pandas as pd
import sqlite3 as lite

# table values
cities = (('Las Vegas', 'NV'),
	('Atlanta', 'GA'),
	('New York City', 'NY'),
    ('Boston', 'MA'),
    ('Chicago', 'IL'),
    ('Miami', 'FL'),
    ('Dallas', 'TX'),
    ('Seattle', 'WA'),
    ('Portland', 'OR'),
    ('San Francisco', 'CA'),
    ('Los Angeles', 'CA'))

weather =(('New York City', 2013, 'July', 'January', 62),
	('Boston', 2013, 'July', 'January', 59),
	('Chicago', 2013, 'July', 'January', 59),
	('Miami', 2013, 'August', 'January', 84),
	('Dallas', 2013, 'July', 'January', 77),
	('Seattle', 2013, 'July', 'January', 61),
	('Portland', 2013, 'July', 'December', 63),
	('San Francisco', 2013, 'September', 'December', 64),
	('Los Angeles', 2013, 'September', 'December', 75),
	('Las Vegas', 2013, 'July', 'December', 95),
	('Atlanta', 2013, 'July', 'January', 82))

#Connect to database
con = lite.connect('getting-started.db') #Check if there's a way to change the db name

with con:
	cur = con.cursor()
# Delete previous tables - I don't find a way to do all at once
	cur.execute("DROP TABLE IF EXISTS weather")
	cur.execute("DROP TABLE IF EXISTS cities")
	cur.execute("DROP TABLE IF EXISTS cities_copy")
# Create tables
	cur.execute("CREATE TABLE cities (name text, state text)")
	cur.execute("CREATE TABLE weather (city text, year integer, warm_month text, cold_month text, average_high integer)")
# Insert values
	cur.executemany("INSERT INTO cities VALUES(?,?)", cities)
	cur.executemany("INSERT INTO weather VALUES(?,?,?,?,?)", weather)
# Join and load into Pandas
cities_weather = pd.read_sql_query("SELECT name, state, year, warm_month, cold_month, average_high FROM cities INNER JOIN weather ON name = city", con)

# Get input from user
print("Please, indicate a month of the year to see warmest cities in that month:")
month = raw_input()

if month == 'January' or month == 'February' or month == 'March' or month == 'April' or month =='May' or month == 'June' or month == 'July' or month == 'August' or month == 'September' or month == 'October' or month == 'November' or month == 'December':
	if cities_weather.warm_month.loc[cities_weather['warm_month'] == month].count() > 0: #Dataframe.empy could also work, didn't have time to check it!
		print("the cities that are warmest in {} are, from warmest to coldest: \n {}".format(month, cities_weather[['name', 'state', 'average_high']].loc[cities_weather['warm_month'] == month].sort_values(by='average_high', ascending=False).to_string(columns=['name', 'state'], index=False, header=False)))
	else:
		print("Sorry, no city has {} as its warmest_month".format(month))
else:
	print("Dude, that's not a month!")


# con.close() -- SHOULD I CLOSE THE CONEXION? I've read I should on the internet but I'm not sure of the implications