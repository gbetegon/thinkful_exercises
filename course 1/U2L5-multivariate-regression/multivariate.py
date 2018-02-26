import pandas as pd
import numpy as np
import statsmodels.api as sm
import statsmodels.formula.api as smf
import matplotlib.pyplot as plt


loansData = pd.read_csv('/Users/Stephanie/downloads/LoanStats3a.csv', skiprows=1)

subloansData = pd.DataFrame(columns = ['Interest.Rate','Annual.Income','Home.Ownership.Raw'])
subloansData['Interest.Rate'] = loansData['int_rate']
subloansData['Annual.Income'] = loansData['annual_inc']
subloansData['Home.Ownership.Raw'] = loansData['home_ownership']
subloansData = subloansData.set_index(loansData['id'])

subloansData.dropna(inplace=True)

subloansData['Interest.Rate'] = subloansData['Interest.Rate'].map(lambda x: float(x[:-1]))
subloansData['Home.Ownership'] = subloansData['Home.Ownership.Raw'].map(lambda x: 1 if x == 'OWN' or x == 'MORTGAGE' else 0)

# spot checking
print(subloansData[(subloansData['Home.Ownership.Raw'] == 'OWN') | (subloansData['Home.Ownership.Raw'] == 'MORTGAGE')].head())
print(subloansData[(subloansData['Home.Ownership.Raw'] == 'NONE') | (subloansData['Home.Ownership.Raw'] == 'OTHER') | (subloansData['Home.Ownership.Raw'] == 'RENT')].head())

# model with anual income
X = sm.add_constant(subloansData['Annual.Income']) #Q1, Q2
model = sm.OLS(subloansData['Interest.Rate'], X)
f = model.fit()
print(f.summary())

# model with anual income and home ownership
X2 = sm.add_constant(subloansData[['Annual.Income', 'Home.Ownership']])
model_2 = sm.OLS(subloansData['Interest.Rate'], X2)
f2 = model_2.fit()
print(f2.summary())

# add interaction
subloansData['Interaction'] = subloansData['Annual.Income'] * subloansData['Home.Ownership'] #Q3
X3 = sm.add_constant(subloansData[['Annual.Income', 'Home.Ownership', 'Interaction']])
model_interaction = sm.OLS(subloansData['Interest.Rate'], X3)
f3 = model_interaction.fit()
print(f3.summary())

subloansData2 = pd.DataFrame(columns = ['Interest','Annual','Home'])
subloansData2['Interest'] = subloansData['Interest.Rate']
subloansData2['Annual'] = subloansData['Annual.Income']
subloansData2['Home'] = subloansData['Home.Ownership']

est = smf.ols(formula='Interest ~ Annual * Home', data=subloansData2).fit()
print(est.summary())

# check correlation between the varibles
print(subloansData.corr())

df = subloansData[subloansData['Annual.Income'] < 100000]

pd.scatter_matrix(df[['Interest.Rate', 'Annual.Income', 'Home.Ownership']])
plt.show()

#QUESTIONS:
#Q1: line 25. According to my model none of the ind variables explain significally the interest.rate (vey low R2), is that correct??
#    what should be the result?
#Q2: line 25. I get this warning: "The condition number is large, 2.19e+05. This might indicate that there are
#    strong multicollinearity or other numerical problems." Using pearson correlation I don't find a significative correlation
#    between the independant variables. Am I missing something? I've read I should use the variance inflation factor (VIF) to check it
#    but I don't know how to do it in Python, any ideas?
#Q3: line 37. Is the interaction correct? 



