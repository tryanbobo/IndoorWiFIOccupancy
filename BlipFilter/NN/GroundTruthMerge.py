import pandas as pd

wifiDataFile = r'C:\Users\tb1302\OneDrive - Texas State University\IndStudy_Bobo\spring2023\NeuroNet\output\Preprocessed_GT.bobo_23_03_11_to_23_03_22.csv'
gtDataFile = r"C:\Users\tb1302\OneDrive - Texas State University\IndStudy_Bobo\spring2023\NeuroNet\grouthTruthv2.csv"

dfWifi = pd.read_csv(wifiDataFile)
dfGt = pd.read_csv(gtDataFile)

#convert to Datetime
dfWifi['Datetime'] = pd.to_datetime(dfWifi['_time']).dt.tz_localize(None)
dfWifi['Datetime1'] = pd.to_datetime(dfWifi['_time'])
print(dfWifi.dtypes)

dfGt["StartTime"] = pd.to_datetime(dfGt["StartTime"]).dt.tz_localize(None)
dfGt["EndTime"] = pd.to_datetime(dfGt["EndTime"]).dt.tz_localize(None)
print(dfGt)
print(dfGt.dtypes)

#add a new column for the ground truth data
dfWifi["GroundTruthFloor"] = None

#loop through each row in the GT data

for _, gt_row in dfGt.iterrows():
    start_time = gt_row["StartTime"]
    end_time = gt_row["EndTime"]
    floor = gt_row["Floor"]

    #Loop through each row in the wifi data
    for index, wifi_row in dfWifi.iterrows():
        wifi_time = wifi_row['Datetime']

        #chech if the wifi timestamp is within the ground truth time range
        if start_time <= wifi_time <= end_time:
            dfWifi.at[index, "GroundTruthFloor"] = floor


#save data
dfWifi.to_csv(r"C:\Users\tb1302\OneDrive - Texas State University\IndStudy_Bobo\spring2023\NeuroNet\output\GtMerged.csv", index=False)


