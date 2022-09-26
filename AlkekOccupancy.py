import pandas as pd
import matplotlib.pyplot as plt

# read excel file
data = pd.read_excel (r'C:\Users\tb1302\OneDrive - Texas State University\IndStudy_Bobo\fall2022\Alkek\OccupancyCounter\Alkek Daily by hour with totals 2022-09-13 07_00 AM.xlsx', sheet_name='Totals By Hour')
# create dataframe from excel file
df = pd.DataFrame(data, columns= ['Location Name','Record Date', 'Total Ins', 'Total Outs'])
print(df)

df.plot(kind= 'line',x= 'Record Date')

plt.plot(df['Total Ins'])
plt.plot(df['Total Outs'])

plt.ylabel('Number of Ins and Outs')
# set the title
plt.title(r"Hourly In and Out Measurements")

# show the plot
plt.show()

