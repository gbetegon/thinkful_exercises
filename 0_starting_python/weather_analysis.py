import sqlite3 as lite
import pandas as pd
import matplotlib.pyplot as plt
import datetime

# Connet to database and read data to DataFrame:
con = lite.connect('weather.db')
cur = con.cursor()

df = pd.read_sql_query('SELECT * FROM daily_temp ORDER BY day',con, index_col='day')

df.index = df.index.map(lambda x: datetime.datetime.fromtimestamp(x).strftime('%Y-%m-%d'))
df.index = pd.to_datetime(df.index)

df.plot(title='Daily Temperatures', legend=True)
plt.show()