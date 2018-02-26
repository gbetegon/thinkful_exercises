import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import statsmodels.api as sm

# LESSON 3.2 - Data extraction, cleaning, histogram and scatter-matrix

loansData = pd.read_csv('https://github.com/Thinkful-Ed/curric-data-001-data-sets/raw/master/loans/loansData.csv')

loansData['Interest.Rate'] = map(lambda x: round(float(x[:-1]), 4), loansData['Interest.Rate'])
loansData['Loan.Length'] = map(lambda x: int(x[:-7]), loansData['Loan.Length'])
loansData['FICO.Score'] = map(lambda x: int(x[:3]), loansData['FICO.Range'])

print(loansData[['Interest.Rate', 'Loan.Length', 'FICO.Range', 'FICO.Score']][0:5])

plt.figure()
p = loansData['FICO.Score'].hist()
plt.show()

# plt.figure() # QUESTION: Why if I include this line I get an empty graph at the end?
# a = pd.scatter_matrix(loansData, alpha=0.05, figsize=(10, 10)) # NOTE: I don't get a density plot but the histogram as I should apparently
# a = pd.scatter_matrix(loansData, alpha=0.05, figsize=(10,10), diagonal='hist')
pd.scatter_matrix(loansData, alpha=0.05, figsize=(10,10), diagonal='hist')
plt.show()

# LESSON 3.3 - Linear Regression Analysis

intrate = loansData['Interest.Rate']
loanamt = loansData['Amount.Requested']
fico = loansData['FICO.Score']

## When we extract a column from a DataFrame, it's returned as a Series datatype. You want to reshape the data like this: WHY. YOU GET THE SAME RESULT SKIPPING THIS STEP???
# dependent variable
y = np.matrix(intrate).transpose()

# independent variable
x1 = np.matrix(fico).transpose()
x2 = np.matrix(loanamt).transpose()
x = np.column_stack([x1, x2])

# linear model -- ISN'T THIS A MULTIVARIATE REGRESSION SINCE IT HAS TWO IND. VARIABLES??
X = sm.add_constant(x)
model = sm.OLS(y,X)
f = model.fit()

print(f.summary()) # NOTE: My results slightly differ from Thinkful, Why?

loansData.to_csv('loansData_clean.csv', header=True, index=False)