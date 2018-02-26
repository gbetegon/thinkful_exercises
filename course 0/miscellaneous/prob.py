import collections
import matplotlib.pyplot as plt
import scipy.stats as stats

#Data used for the challenge
lesson_data = [1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 3, 4, 4, 4, 4, 5, 6, 6, 6, 7, 7, 7, 7, 7, 7, 7, 7, 8, 8, 9, 9]

# Output numbers' frequencies
data_count = collections.Counter(lesson_data)
count_sum = sum(data_count.values()) 
for k,v in data_count.iteritems():
  print("The frequency of number " + str(k) + " is " + str(float(v) / count_sum))

# Create and save boxplot, histogram and QQ Plot
plt.figure("boxplot")
plt.boxplot(lesson_data)
plt.show()

plt.figure("histogram")
plt.hist(lesson_data, histtype='bar')
plt.show()

plt.figure("QQ Plot")
graph_QQ_Plot = stats.probplot(lesson_data, dist="norm", plot=plt)
plt.show()

