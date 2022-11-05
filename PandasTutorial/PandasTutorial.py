import pandas as pd


d_parser = lambda x: pd.datetime.strptime(x, '%Y-%m-%d %I-%p')
df = pd.read_csv('ETH_1h.csv', parse_dates=['Date'], date_parser=d_parser)


#print(df.loc[0, 'Date'])

#print(df.loc[0, 'Date'].day_name())
df['DayOfWeek'] = df['Date'].dt.day_name()

print(df['Date'].min())

print(df['Date'].max() - df['Date'].min())
########################################################
print(df.head())
print(df.shape)