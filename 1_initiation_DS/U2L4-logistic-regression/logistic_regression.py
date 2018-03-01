import pandas as pd
import statsmodels.api as sm
import math
import matplotlib.pyplot as plt

# Load the data
loansData = pd.read_csv('/Users/Stephanie/Desktop/thinkful/projects/linear-regression/loansData_clean.csv')

# Add a column to your dataframe indicating whether the interest rate is < 12%.
loansData['IR_TF'] = loansData['Interest.Rate'].map(lambda x: 1 if x >= 12 else 0) #Q1

# Spot check
print(loansData[['Interest.Rate', 'IR_TF']].head())
print(loansData[loansData['Interest.Rate'] == 10].head())
print(loansData[loansData['Interest.Rate'] > 12].head())

# Create intercept constant
intercept = [1.0] * len(loansData)
loansData['Intercept'] = intercept

# create column with independant variables
ind_vars = ['FICO.Score', 'Amount.Requested', 'Intercept']

# Define and fit the logistic regression model.

logit = sm.Logit(loansData['IR_TF'], loansData[ind_vars])
result = logit.fit()

# Get fitted coefficients

coeff = result.params
print(coeff)

# Build logistic function

def logistic_function(FicoScore, LoanAmount):
	p = 1 / (1 + math.exp(coeff[2] + coeff[0]*FicoScore + coeff[1]*LoanAmount))
	if p >= 0.70:
		prediction = 1
	else:
		prediction = 0
	print("the probability of obtaining a loan for {}$ with an interest below 12% with a Fico Score of {} is {} - odds {} to 1. Prediction: {}".format(LoanAmount, FicoScore, round(p, 2), round(p/(1-p), 2), prediction))

logistic_function(720, 10000)

pd.scatter_matrix(loansData[['Interest.Rate', 'FICO.Score', 'Amount.Requested']]) #Q3
plt.show()

# QUESTIONS
# Q1: line 10: Using 1: int. rate, >= 12 0: int. rate < 12 we get the opposite coefficients as the ones shown in the curriculum.
#     I think it might be a typo
# Q3: line 46: What's the best way to plot the data in this case and why? 
# Q2: How to build prediction function? (10 point of the lesson)
