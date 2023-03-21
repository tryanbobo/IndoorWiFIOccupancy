import pandas as pd
import numpy as np

path = r'C:\Users\tb1302\OneDrive - Texas State University\IndStudy_Bobo\Data\WifiData'
df = pd.read_csv(path + r'\bobo_23_02_19_to_23_03_04.anon.csv')
pd.set_option('display.max_columns', None)

########################################################################
'''
Preprocessing
'''
########################################################################
#raw record count
print('Raw record count: ', len(df.index), ':0')

#dropping unnecessary columns
df = df.drop(['vlan', 'action', 'hostname', 'rssi', 'receivedSignalStrength', 'instantaneous_rssi', 'client_ip', 'apMac'], axis=1)

#remove duplicates
df = df.drop_duplicates()
print('Record count with duplicates removed: ', len(df.index), ':)')

#remove outdoor AP ...should be 314,819 records
df = df[df['AP_Name'] != 'ODAP0.ALK0']
print('Record count with outdoor AP removed: ', len(df.index), ':))')


#replace values in the 'AP_Name' column
df['AP_Name'] = df['AP_Name'].replace({
    'AP0.ALK0.M100': 'AP0.ALK0.100M',
    'AP0.ALK0.MechRm': 'AP0.ALK0.100M2',
    'ap0.alkek.e103': 'AP0.ALK0.103E',
    'ap0.alkek.100': 'AP0.ALK0.100',
    'ap0.alk0.719h': 'AP0.ALK0.719H'
})

#capitalize all records in the 'AP_Name' column
df['AP_Name'] = df['AP_Name'].str.upper()

#select the digit that indicates floor from AP_Name and add it to a new column "Floor"
# AI generated re "\.(\d)(?=\d{2}$)", maybe try this?
df['Floor'] = df['AP_Name'].str.extract('^[^\.]*\.[^\.]*\.[^\.]*?([0-9])', expand=True)

#convert _Time (object) to Datetime(datetime64[ns...]
df['Datetime'] = pd.to_datetime(df['_time'])
print(df.dtypes)

print("Record count at end of preprocessing: ", len(df.index))
#print(df)



df.to_csv(path + r'\output\Preprocessed.alk_data_23_02_19_to_23_04_03.csv')