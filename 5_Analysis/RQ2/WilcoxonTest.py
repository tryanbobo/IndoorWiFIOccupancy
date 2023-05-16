import numpy as np
import pandas as pd
from scipy import stats
import matplotlib.pyplot as plt
# load csv files
# Ground truth data with Static Wi-Fi counts:
df = pd.read_csv(r'C:\Users\tb1302\OneDrive - Texas State University\IndStudy_Bobo\Data\WifiData\output\RQ2\GT-Static-DynamicWifi.csv')


# Convert Median_Time to Datetime objects
df["Median_Time"] = pd.to_datetime(df["Median_Time"])

# check if ground truth collection follow a normal distribution
gtShapiroTest = stats.shapiro(df['StaticCount'])
print(f'Shapiro test statistic: {gtShapiroTest[0]}, p-value: {gtShapiroTest[1]}')

# plot histogram
plt.hist(df['StaticCount'], bins='auto', alpha=0.7)
plt.title('Histogram of Ground Truth Counts')
plt.xlabel('StaticCount')
plt.ylabel('Frequency')
plt.show()

# Plot Q-Q plot
stats.probplot(df['StaticCount'], plot=plt)
plt.title('Q-Q plot of Ground Truth Counts')
plt.show()

#Apply Mean Absolute
# Apply Wilcoxon Test between ground truth counts and static wifi counts
# define function to calculate the Mean Absolute Percent Error
def mape(actual, predicted):
    actual, predicted = np.array(actual), np.array(predicted)
    return np.mean(np.abs((actual - predicted) / actual)) * 100

StaticError = mape(df["MedianTotal"], df["StaticCount"])
print('Static Filter Mean Absolute Percentage Error:', StaticError)

DynamicError = mape(df["MedianTotal"], df["DynamicCount"])
print('Dynamic Filter Mean Absolute Percentage Error:', DynamicError)