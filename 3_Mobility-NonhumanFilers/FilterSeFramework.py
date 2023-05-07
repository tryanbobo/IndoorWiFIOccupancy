import pandas as pd
from pprint import pprint


path = r'C:\Users\tb1302\OneDrive - Texas State University\IndStudy_Bobo\Data\sampleData'
#df = pd.read_csv(path + r'\Stack-testData_2022_ytd.csv')
df = pd.read_csv(path + r'\Stack-testData_2022_ytd.csv')

#convert _Time (object) to Datetime(datetime64[ns...]
df['Datetime']=pd.to_datetime(df['Datetime'])

calculated_data = {}

# final_data will store the output calculations
final_data = pd.DataFrame(columns=['_user', 'vlan_role','Floor','Datetime','duration'])

for index, row in df.iterrows():
    # Check to see if user exists in dict - if not, add
    if row['_user'] not in calculated_data:
        calculated_data[row['_user']] = {'last_floor':row['Floor'],'last_time':row['Datetime']}

    # User moved up a floor - calculate the difference and save
    # Check to see if floor is not equal to the previous floor
    elif row['Floor'] != calculated_data[row['_user']]['last_floor']:
        #subtracts the previous user's datetime from the one that changed floor
        duration = row['Datetime'] - calculated_data[row['_user']]['last_time']
        #creates new df
        final_data.loc[len(final_data)] = [row['_user'],row['vlan_role'],calculated_data[row['_user']]['last_floor'],calculated_data[row['_user']]['last_time'],duration]
        # Update the dict with the latest floor data
        calculated_data[row['_user']] = {'last_floor':row['Floor'],'last_time':row['Datetime']}

print(final_data)
pprint(calculated_data)
#saves df as csv
final_data.to_csv(path + '\durationSample.csv')