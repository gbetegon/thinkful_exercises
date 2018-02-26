import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import scipy.stats as stats

# Read loans' data and load into pandas data frame
loansData = pd.read_csv('https://github.com/Thinkful-Ed/curric-data-001-data-sets/raw/master/loans/loansData.csv')

# Clean loans' data
loansData.dropna(inplace=True)

# Box plot
plt.figure()
loansData.boxplot(column=['Amount.Requested', 'Amount.Funded.By.Investors'])
plt.savefig('loansData - Amount requested and funded - Box plot.png')

# Combined histograms
plt.figure()
x = loansData['Amount.Requested']
y = loansData['Amount.Funded.By.Investors']
bins=np.linspace(0, 35000, 10)

plt.hist(x, bins, alpha=0.5, label='Requested') # The output includes this labels
plt.hist(y, bins, alpha=0.5, label='Funded')
plt.legend(loc='upper right')
plt.savefig('loansData - Amount requested and funded - Histogram.png')


# 2nd option - Separated histograms (currently not used):
#loansData.hist(column=['Amount.Requested', 'Amount.Funded.By.Investors'])
#plt.savefig('loansData - Amount requested and funded - Histogram.png')

# QQ plot
plt.figure()
graph = stats.probplot(loansData['Amount.Requested'], dist="norm", plot=plt) #It would be interesting to included amount requested but I think this formula only allows one dimension
plt.savefig('loansData - Amount requested - QQ plot.png')

# Comparison of main statistical variables
data_description = loansData[['Amount.Requested', 'Amount.Funded.By.Investors']].describe()

# What percentage of loands are funded below 90% of the amount requested?
loansData['Fund_Percentage'] = (loansData['Amount.Requested'] - loansData['Amount.Funded.By.Investors'])/loansData['Amount.Funded.By.Investors']
less_funded_loands = sum(1 for x in loansData.Fund_Percentage if x > 0.1)
percentage_of_less_funded_loands = (float(less_funded_loands) / len(loansData.Fund_Percentage))*100

#Results description:
print(data_description)
print("The amount requested and the amount funded by investors follows almost the same distribution, right skewed.")
print("Logically, for every loan the amount funded has to be the same as the amount requested or lower. This can be seen in the box plot and the mean.")
print("However, this difference is very little: Only {} per cent of all loans are funded below 90 per cent of the requested amount".format(percentage_of_less_funded_loands))
