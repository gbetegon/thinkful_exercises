import matplotlib.pyplot as plt
import pandas as pd
from scipy import stats
import collections

# Load the reduced version of the Lending Club Dataset
loansData = pd.read_csv('https://github.com/Thinkful-Ed/curric-data-001-data-sets/raw/master/loans/loansData.csv')
# Drop null rows
loansData.dropna(inplace=True)

freq = collections.Counter(loansData['Open.CREDIT.Lines'])

chi, p = stats.chisquare(freq.values())

print(chi, p)