import pandas as pd
from IPython.display import display
import matplotlib.pyplot as plt

path = r'C:\Users\tb1302\OneDrive - Texas State University\IndStudy_Bobo\Data\sampleData'
"""#df = pd.read_csv(path + r'\Stack-testData_2022_ytd.csv')
df = pd.read_csv(path + r'\durationSample.csv')

df = df.set_index('Datetime')
df.index = pd.to_datetime(df.index)
print(df.dtypes)
dfR = df.groupby(['_user', 'vlan_role', 'Floor']).resample('30T').sum()
#dfR = df.resample('30T').sum()


dfR.to_csv(path + r'\resampleTest\resample-30T.csv
"""
######################################################################

df2 = pd.read_csv(path + r'\Stack-testData_2022_ytd.csv')
df2 = df2.set_index('Datetime')
df2.index = pd.to_datetime(df2.index)

dfR = df2.groupby(['Floor', '_user']).resample('30T').sum()


dfR.to_csv(path + r'\resampleTest\resample-30T2.csv')
#display(dfR)
#
#dfR.plot('_user')
#plt.show()

