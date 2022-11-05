import pandas as pd
import numpy as np
import datetime
import numpy as np
from sklearn.datasets import load_iris

path = r'C:\Users\tb1302\OneDrive - Texas State University\IndStudy_Bobo\Data\sampleData'
df = pd.read_csv(path + r'\testData_2022_ytd.csv')

#selects the digit that indicates floor from AP_Name and adds it to a new column "Floor"
df['Floor'] = df['AP_Name'].str.extract('^[^\.]*\.[^\.]*\.[^\.]*?([0-9])', expand=True)

#convert _Time (object) to Datetime(datetime64[ns...]
df['Datetime']=pd.to_datetime(df['_time'])
print(df.dtypes)



df["duration"] = df.groupby("Floor")["Datetime"].transform(lambda x: np.ptp(x.to_numpy()))
print(df)

####################################################################################

# position << this is a list of the locations of the Datetime column within the larger dataframe
# df.iloc[0, position] << this is the first (0) position in the list of positions
# df.iloc[1:, position] << this is the second (1) to the last position in the list of positions

"""position = df.columns.get_loc('Datetime')
df['Elapsed'] = df.iloc[1:, position] - df.iat[0, position]"""

####################################################################################
#duration testing
"""startTime = df.Datetime.loc[0]
endTime = df.Datetime.loc[5]
print('time elapsed: ', endTime-startTime)"""

####################################################################################
# poor attempt at adapting a method for measuring duration
"""def gb(df, *args, **kwargs):
    for k, g, in df.groupby(*args,**kwargs):
        splt = np.split(g, np.where(np.diff(g.index.values)!=1)[0]+1)
        for subg in splt:
            if len(subg) >=2: yield k, subg

group_args = ['_user', df['_time'].apply(lambda x:x.date()),'Floor']

for key, grp in gb(df,group_args, sort=False):
    print(key)
    print(grp)
    print('-'*10)"""

#####################################################################################

#saves df as csv
df.to_csv(path + '\df_out.csv')

#with pd.option_context('display.max_rows', None, 'display.max_columns', None):
    #print(df)

print(df)