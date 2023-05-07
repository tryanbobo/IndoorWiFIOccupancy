import warnings
import pandas as pd
from scipy.stats import mode
from scipy.stats import shapiro
from scipy.stats import ks_2samp
from sklearn.metrics import mean_absolute_error, mean_squared_error
import matplotlib.pyplot as plt

warnings.simplefilter(action='ignore', category=FutureWarning)
# Replace the file path with the path to your CSV file
path = r'C:\Users\tb1302\OneDrive - Texas State University\IndStudy_Bobo\spring2023\NeuroNet\output'
file = path + r'\GtMerged.csv'
# Read the CSV file into a DataFrame
df = pd.read_csv(file)

df = df.drop(columns=['Unnamed: 0', 'action', 'mac_address'], axis=1)

# Set DateTime as index
df.set_index('Datetime', inplace=True)

df = df.drop_duplicates()

df = df.sort_values(by=['user', 'Datetime'])

# loop through
for win in range(1, 10):
    df['CorrectedFloor'] = df['Floor'].rolling(window=win).apply(lambda x: mode(x)[0])

    df_clean = df.dropna(subset=['GroundTruthFloor', 'CorrectedFloor'])


    mse = mean_squared_error(df_clean['GroundTruthFloor'], df_clean['CorrectedFloor'])
    mae= mean_absolute_error(df_clean['GroundTruthFloor'], df_clean['CorrectedFloor'])
    print('For window size {}: MSE = {}, MAE = {}'.format(win, mse, mae))
    #print(df_clean[['GroundTruthFloor', 'CorrectedFloor']])
    #stat, p = ks_2samp(wifiFloor, gtFloor)
    #print('with a window size of {}."p" score is: '.format(win), p)


    if win == 4:
        df.to_csv(path + '\SW-Mode-Win{}_out.csv'.format(win), index=False)


# perform Kolmogorov-Smirnov to compare distributions of ground truth data and wifi generated data.





print(df)
####################################################################################
# distribution test
# plot a histogram
df['Floor'].plot(kind='hist', bins=7)
plt.show()
# plot a box plot
df['Floor'].plot(kind='box')
plt.show()

#Perform the shapiro-wilk test
stat, p = shapiro(df['Floor'])

# check p-value
alpha = 0.05
if p > alpha:
    print('The data appears to follow a normal distribution.')
else:
    print('The data appears to be nonparametric')


#df.to_csv(path + '\SW-Mode2_out.csv', index=False)

