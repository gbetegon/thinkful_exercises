import datetime
import requests
import sqlite3 as lite

# Create dictionary with cities
cities = { "Denver": '39.761850,-104.881105',
           "New_Orleans": '30.053420,-89.934502',
           "New_York": '40.663619,-73.938589',
           "San_Francisco": '37.727239,-123.032229',
           "Seattle": '47.620499,-122.350876'
           }

key = "4e98572ec6b467167ec0d328f8366dc4"

# Format time to unix
end_date = datetime.datetime.now()
query_date = datetime.datetime.now() - datetime.timedelta(days=30)

# Create database and table

con = lite.connect('weather.db')
cur = con.cursor()

with con:
	cur.execute('DROP TABLE IF EXISTS daily_temp')
	cur.execute('CREATE TABLE daily_temp (day INT, Denver INT, New_Orleans INT, New_York INT, San_Francisco INT, Seattle INT)') #WHY NOT PRIMARY KEY? CHECK

with con:
    while query_date < end_date:
        cur.execute("INSERT INTO daily_temp(day) VALUES (?)", (int(query_date.strftime('%s')),))
        query_date += datetime.timedelta(days=1)
    for k,v in cities.iteritems():
    	query_date = end_date - datetime.timedelta(days=30)
    	while query_date < end_date:
    		r = requests.get("https://api.darksky.net/forecast/{}/{},{}".format(key, v, query_date.strftime('%Y-%m-%dT12:00:00')))
    		#r = requests.get(url + v + ',' +  query_date.strftime('%Y-%m-%dT12:00:00'))
    		with con:
    			cur.execute('UPDATE daily_temp SET ' + k + ' = ' + str(r.json()['daily']['data'][0]['temperatureMax']) + ' WHERE day = ' + query_date.strftime('%s'))
        	query_date += datetime.timedelta(days=1)

con.close()
	