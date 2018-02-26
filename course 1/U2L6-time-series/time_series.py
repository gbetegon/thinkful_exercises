import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import statsmodels.api as sm

#load data
df = pd.read_csv('/Users/Stephanie/downloads/LoanStats3a.csv', header=1, low_memory=False) #I've read is deprecated, why do we use it?

# convert issue date column to datetime

df['issue_d_format'] = pd.to_datetime(df['issue_d']) #Q1
dfts = df.set_index('issue_d_format')
year_month_summary = dfts.groupby(lambda x: x).count()
loan_count_summary = year_month_summary['issue_d']
print(loan_count_summary.head())

# Plot time series

plt.plot(loan_count_summary)
plt.show()

# Difference times series and plot
loan_count_summary_diff = loan_count_summary.diff()
loan_count_summary_diff = loan_count_summary_diff.fillna(0)
plt.plot(loan_count_summary_diff)
plt.show()

# Run ACF and PACF for series and differenced series
sm.graphics.tsa.plot_acf(loan_count_summary)
plt.show()
sm.graphics.tsa.plot_pacf(loan_count_summary)
plt.show()

sm.graphics.tsa.plot_acf(loan_count_summary_diff)
plt.show()
sm.graphics.tsa.plot_pacf(loan_count_summary_diff)
plt.show()

# QUESTIONS
# Q1: line 11. I've seen this code for the exercise:

#year_month_summary = dfts.groupby(lambda x: x.year * 100 + x.month).count()
#loan_count_summary = year_month_summary['issue_d']
#print(loan_count_summary.head())

# I don't understand what's the goal of the code. It messes up the X axe and looks more complex. Am I missing something?



