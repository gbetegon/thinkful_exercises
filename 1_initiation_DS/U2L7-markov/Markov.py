# https://github.com/sebastiandres/DataScienceExamples/blob/master/Lorenzo/Session03/U2L8A1_markov_chain.py
# I think he makes a mistake in line 34 when writing the numpy matrix (rows and columns are not aligned in his case)

import pandas as pd
import numpy as np

np.set_printoptions(suppress=True, precision=4)

markov = pd.DataFrame({'bear market': [.075, .8, .25],
	'bull market': [.9, .15, .25],
	'stagnation market': [.025, .05, .5]
	},
	index=["bear market", "bull market", "stagnation market"])
print(markov)

A = np.array([[.075, .900, .025],
	[.800, .150, .050],
	[.250, .250, .500]])
 
B = markov.as_matrix() #.T (so that rows sum 1 if neccesary to transpose)

print A
print ""
print B
print ""
print np.dot(A,A)
print ""
print np.dot(B,B)
print ""
print np.linalg.matrix_power(A,2+1)
print np.linalg.matrix_power(A,5+1)
print np.linalg.matrix_power(A,10+1)
print np.linalg.matrix_power(A,30+1)
