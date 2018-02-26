import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import statsmodels.api as sm

#load data
glob_temp = pd.read_csv('/Users/Stephanie/Downloads/GlobalLandTemperatures/GlobalTemperatures.csv')
glob_temp['dt'] = pd.to_datetime(glob_temp['dt'])
glob_temp = glob_temp.set_index('dt')
month_land_avrg = glob_temp['LandAverageTemperature']
year_land_avrg = glob_temp['LandAverageTemperature'].groupby(glob_temp.index.year).mean()


#plot land average temperature

# the monthly data doesn't show any trend
plt.figure('Land Average Temperature')
plt.plot(month_land_avrg)
plt.show()

# but when we plot the average temperature by year there's a clear increse over time
plt.figure('Yearly Land Average Temperature') #Q1 and 2
plt.plot(year_land_avrg)
plt.show()

# difference yearly series
year_land_avrg_diff = year_land_avrg.diff()
year_land_avrg_diff = year_land_avrg_diff.fillna(0)
plt.figure('Differenced Yearly Series')
plt.plot(year_land_avrg_diff)
plt.show()

# Run ACF and PACF for yearly series and differenced series
sm.graphics.tsa.plot_acf(year_land_avrg)
plt.show()

sm.graphics.tsa.plot_pacf(year_land_avrg)
plt.show()

sm.graphics.tsa.plot_acf(year_land_avrg_diff)
plt.show()

sm.graphics.tsa.plot_pacf(year_land_avrg_diff)
plt.show()

# INTERPRETATION

# I think there might have been a problem during the first years and the measures might not be that reliable 

# QUESTIONS
#Q1: line 22 - I've tried to plot both graphs together but I can't because of different dimensions.
#              I've tried different ways but always got blocked. Any ideas?
#Q2: line 22 - Would be a moving average more appropiate than just using the average?


